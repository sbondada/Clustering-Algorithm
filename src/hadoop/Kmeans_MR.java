import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.Random;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.SequenceFile;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Counter;
import org.apache.hadoop.mapreduce.Counters;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class Kmeans {
	public static enum UPDATECOUNTER {
		isUPDATED;
	};

	static class KmeansMapper extends Mapper<LongWritable, Text, Text, Text> {
		public static ArrayList<float[]> centroidArr = new ArrayList<float[]>();

		// store the centroid values in float array centroidArr. It will hold
		// the dimensions of the input file

		@Override
		protected void setup(Context context) throws IOException,
				InterruptedException {
			super.setup(context);
			Configuration conf = context.getConfiguration();
			Path kmeans = new Path(conf.get("centroid"));
			FileSystem fs = FileSystem.get(conf);
			SequenceFile.Reader reader = new SequenceFile.Reader(fs, kmeans,
					conf);
			Text key = new Text();
			Text value = new Text();

			// It will loop through the centroids eg. loop 3 times if clusters
			// required are 3
			while (reader.next(key, value)) {
				String line = value.toString();
				System.out.println("Sequesnce: " + line + ":" + key);
				String tokens[] = line.split("\\s+");

				// dimensions of the value list or gene values in this case
				float[] temp = new float[tokens.length];

				// it will loop through all the dimension values for a
				// particular centroid
				for (int i = 0; i < tokens.length; i++) {
					/*
					 * if(i==1){ continue; }
					 */
					temp[i] = Float.parseFloat(tokens[i]);
				}
				centroidArr.add(temp);
			}
			reader.close();
		}

		@Override
		public void map(LongWritable key, Text value, Context context)
				throws IOException, InterruptedException {

			String valuesStr[];
			float valuesFlt[];
			int totalValues;
			StringBuffer valueSB = new StringBuffer();

			valuesStr = value.toString().split("\\s+");
			totalValues = valuesStr.length;
			valuesFlt = new float[totalValues - 1];
			int count=0;
			for (int j = 0; j < totalValues; j++) {
				if (j == 1) {
					continue;
				}

				valueSB.append(valuesStr[j].trim());
				if (j != totalValues - 1) {
					valueSB.append("\t");
				}

				if(j==0){
				    continue;
				}
				valuesFlt[count] = Float.parseFloat(valuesStr[j].trim());
				count++;

			}

			// we have all the gene values in a float array
			float min = 0;
			int centroidNum = 0;

			// context iterate for all the centroids and check the distance
			for (int centNum = 0; centNum < centroidArr.size(); centNum++) {
				// load the centroid values into float array
				float[] currCentroidValuesFlt = centroidArr.get(centNum);
				float sum = 0;

				for (int valueIndex = 0; valueIndex < currCentroidValuesFlt.length; valueIndex++) {
					sum += Math
							.pow((valuesFlt[valueIndex] - currCentroidValuesFlt[valueIndex]),
									2);
				}

				sum = (float) Math.sqrt(sum);
				if (centNum == 0) {
					min = sum;
				}
				// update the minimum distance and the centroid number
				if (sum < min) {
					min = sum;
					centroidNum = centNum;
				}
			}

			StringBuffer sb = new StringBuffer();
			// String keyB = new String(valueSB);
			Text emitValue = new Text(valueSB.toString());
			float[] emitcentroid = centroidArr.get(centroidNum);
			for (int i = 0; i < emitcentroid.length; i++) {
				sb.append(emitcentroid[i]);
				if (i != valuesFlt.length - 1) {
					sb.append("\t");
				}
			}
			// String s = new String(sb);
			Text keyCentroid = new Text();
			keyCentroid.set(sb.toString());

			context.write(keyCentroid, emitValue);

		}
	}

	static class KmeansReducer extends Reducer<Text, Text, Text, Text> {
		ArrayList<String> newCentroids = new ArrayList<String>();

		@Override
		public void reduce(Text key, Iterable<Text> values, Context context)
				throws IOException, InterruptedException {

			ArrayList<Text> tempValues = new ArrayList<Text>();

			int numOfValues = key.toString().split("\\s+").length;
			float means[] = new float[numOfValues];
			float sum[] = new float[numOfValues];
			int countUniqueValueObjects = 0;

			ArrayList<float[]> valuesFlt = new ArrayList<float[]>();
			for (Text count : values) {
				Text t = new Text(count.toString());
				tempValues.add(t);
				String tokens[] = count.toString().split("\\s+");

				for (int i = 0; i <(tokens.length-1); i++) {
				    //			if (i != 1) {
						means[i] = Float.parseFloat(tokens[i+1]);
						sum[i] += means[i];
					
				}
				valuesFlt.add(means);
				countUniqueValueObjects++;
			}
			StringBuffer sb = new StringBuffer();
			// update the mean sum of all values
			for (int i = 0; i < numOfValues; i++) {
				sum[i] = sum[i] / countUniqueValueObjects;
				sb.append(sum[i]);
				if (i != numOfValues - 1) {
					sb.append("\t");
				}
			}

			Text newCentroid = new Text(new String(sb));
			newCentroids.add(newCentroid.toString());
			String str = (new Integer(newCentroids.size())).toString();
			Text emitKey = new Text(str);
			// int number;
			if ((key.toString()).compareTo(newCentroid.toString()) != 0) {
				context.getCounter(UPDATECOUNTER.isUPDATED).increment(1);
				// number= context.getCounter(UPDATECOUNTER.isUPDATED);
			}

			for (int j = 0; j < tempValues.size(); j++) {
				context.write(emitKey, tempValues.get(j));
				// use this code if need to display the new centroid values
				// context.write(emitKey, tempValues.get(j));
			}
		}

		/**
		 * Trash the temp data generated during the job
		 */
		@Override
		protected void cleanup(Context context) throws IOException,
				InterruptedException {

			super.cleanup(context);
			Configuration conf = context.getConfiguration();
			Path kmeans = new Path(conf.get("centroid"));
			FileSystem fs = FileSystem.get(conf);
			if (fs.exists(kmeans)) {
				fs.delete(kmeans, true);
			}

			// update the sequence file with new centroid values for next
			// iteration

			final SequenceFile.Writer out = SequenceFile.createWriter(fs,
					context.getConfiguration(), kmeans, Text.class, Text.class);
			for (int i = 0; i < newCentroids.size(); i++) {
				String key = Integer.toString(i);
				Text value = new Text();
				value.set(newCentroids.get(i));
				out.append(new Text(key), value);
			}

		}
	}

	public static void initializeCentroid(Configuration conf, String input,
			Path centroid, FileSystem fs, int numOfClusters) throws IOException {
		if (fs.exists(centroid)) {
			fs.delete(centroid, true);
		}
		// Test statements to be removed
		System.out.println("path from conf is " + conf.get("centroid"));
		System.out.println("centroid path is " + centroid.toString());
		// test end

		/*
		 * Read the random gene values and assign to centroids
		 */
		ArrayList<String[]> clusters = new ArrayList<String[]>();
		String temp;
		String tokens[] = null;
		int k = 0;
		try {
			FileStatus[] status = fs.listStatus(new Path(input));
			for (int i = 0; i < status.length; i++) {
				BufferedReader br = new BufferedReader(new InputStreamReader(
						fs.open(status[i].getPath())));

				int totalRecords = 0;
				while ((temp = br.readLine()) != null) {
					totalRecords++;
				}

				BufferedReader brNew = new BufferedReader(
						new InputStreamReader(fs.open(status[i].getPath())));

				int randRecords[] = new int[numOfClusters];
				Random randGen = new Random();
				for (int u = 0; u < numOfClusters; u++) {
					randRecords[u] = randGen.nextInt(totalRecords);
					System.out.println("valll:" + randRecords[u]);
				}
				int counter = 0;
				while ((temp = brNew.readLine()) != null) {

					if (k == numOfClusters)
						break;

					for (int w = 0; w < numOfClusters; w++) {
						if (counter == randRecords[w]) {
							// System.out.println("Kallo:" + w + ":" + counter);
							tokens = temp.split("\\s+");
							String tempStr[] = new String[(tokens.length - 2)];
							int q = 0;
							for (int tmp = 2; tmp < tokens.length; tmp++) {

									tempStr[q] = tokens[tmp];
									q++;
								
							}
							System.out.println("key " + tempStr[0]+tempStr[1]);

							clusters.add(tempStr);
							k++;
						}

					}
					counter++;
				}
			}
		} catch (Exception e) {
			System.out.println("File not found");
		}
		/*
		 * Now write the choosen centroid values into a sequence file Sequence
		 * file stored in HDFS
		 */
		SequenceFile.Writer centroidWriter = SequenceFile.createWriter(fs,
				conf, centroid, Text.class, Text.class);
		for (int i = 0; i < clusters.size(); i++) {
			String tempClust[] = clusters.get(i);
			
			Text key = new Text();
			key.set(Integer.toString(i));
			StringBuffer sb = new StringBuffer();
			for (int j = 0; j < tempClust.length; j++) {
				sb.append(tempClust[j]);
				if (j != tempClust.length - 1) {
					sb.append("\t");
				}
			}
			System.out.println("in writers " + key.toString() + ":: " + sb);
			String s = new String(sb);
			Text value = new Text();
			value.set(s);
			centroidWriter.append(key, value);
		}
		centroidWriter.close();
	}

	public static void main(String[] args) throws IOException,
			ClassNotFoundException, InterruptedException {
		Configuration conf = new Configuration();
		Path centroid = new Path(args[3] + "//temp.seq");
		conf.set("centroid", centroid.toString());

		FileSystem fs = FileSystem.get(conf);
		// call
		initializeCentroid(conf, args[0], centroid, fs,
				Integer.parseInt(args[2]));

		Job job = new Job(conf, "Kmeans");
		job.setJarByClass(Kmeans.class);
		job.setMapperClass(KmeansMapper.class);
		if (fs.exists(new Path(args[1])))
			fs.delete(new Path(args[1]), true);
		job.setReducerClass(KmeansReducer.class);
		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		job.waitForCompletion(true);

		Counters counter = job.getCounters();
		Counter c1 = counter.findCounter(UPDATECOUNTER.isUPDATED);
		System.out.println(c1.getDisplayName() + ":" + c1.getValue());
		Long totalNodes = c1.getValue();
		int nodes = 0;
		int counter1 = 0;
		// while (c1.getValue() >= 0 && counter1 < 7) {
		while (c1.getValue() >= 0) {
			c1.increment(-1);
			nodes++;
			conf = new Configuration();
			centroid = new Path(args[3] + "//temp.seq");
			conf.set("centroid", centroid.toString());
			job = new Job(conf, "reprocessingMap" + nodes);
			job.setJarByClass(Kmeans.class);
			job.setMapperClass(KmeansMapper.class);
			if (fs.exists(new Path(args[1]))) {
				fs.delete(new Path(args[1]), true);
			}
			job.setReducerClass(KmeansReducer.class);
			job.setInputFormatClass(TextInputFormat.class);
			job.setOutputFormatClass(TextOutputFormat.class);
			FileInputFormat.addInputPath(job, new Path(args[0]));
			FileOutputFormat.setOutputPath(job, new Path(args[1]));
			job.setOutputKeyClass(Text.class);
			job.setOutputValueClass(Text.class);
			job.waitForCompletion(true);
			c1 = counter.findCounter(UPDATECOUNTER.isUPDATED);
			//System.out.println(c1.getDisplayName() + ":" + c1.getValue());
			counter1++;
			System.out.println("Iterations number : " + (counter1 + 1));

		}
	}

}
