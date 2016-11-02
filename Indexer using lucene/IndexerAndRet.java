
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.Fields;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.MultiFields;
import org.apache.lucene.index.Term;
import org.apache.lucene.index.Terms;
import org.apache.lucene.index.TermsEnum;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class IndexerAndRet {
	private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
	private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

	private IndexWriter writer;
	private ArrayList<File> queue = new ArrayList<File>();

	public static void main(String[] args) throws IOException {
		System.out
		.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

		String indexLocation = null;
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		String s = br.readLine();

		IndexerAndRet indexer = null;
		try {
			indexLocation = s;
			indexer = new IndexerAndRet(s);
		} catch (Exception ex) {
			System.out.println("Cannot create index..." + ex.getMessage());
			System.exit(-1);
		}

		// ===================================================
		// read input from user until he enters q for quit
		// ===================================================
		while (!s.equalsIgnoreCase("q")) {
			try {
				System.out
				.println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
				System.out
				.println("[Acceptable file types: .xml, .html, .html, .txt]");
				s = br.readLine();
				if (s.equalsIgnoreCase("q")) {
					break;
				}

				// try to add file into the index
				indexer.indexFileOrDirectory(s);
			} catch (Exception e) {
				System.out.println("Error indexing " + s + " : "
						+ e.getMessage());
			}
		}

		// ===================================================
		// after adding, we always have to call the
		// closeIndex, otherwise the index is not created
		// ===================================================
		indexer.closeIndex();

		// =========================================================
		// Now search
		// =========================================================
		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
				indexLocation)));
		IndexSearcher searcher = new IndexSearcher(reader);
		TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);

		// function calling for term_to_tf
		s="";
		Boolean buildList = true;
		while (buildList == true) {
			System.out.println("Do you wish to build a list of (unique term, term_frequency) "
					+ "for this index, sorted by frequency?(y=yes,n=no):");
			s = br.readLine();
			if (s.equalsIgnoreCase("y")) {
				System.out
				.println("Enter the FULL path(Path/folder should already exist) where you need to write the list:(e.g. /Usr/index or c:\\temp\\index)");
				String file_path = br.readLine();
				buildList = termToTfCalc(reader,file_path); 
			}
			else if (s.equalsIgnoreCase("n")){
				buildList = false;
			}
			else{
				System.out
				.println("Wrong Input encountered, please try again.");
			}
		}
		s = "";
		while (!s.equalsIgnoreCase("q")) {
			try {
				System.out.println("Enter the search query (q=quit):");
				s = br.readLine();
				if (s.equalsIgnoreCase("q")) {
					break;
				}
				String query_text = s;
				Query q = new QueryParser(Version.LUCENE_47, "contents",
						sAnalyzer).parse(s);
				searcher.search(q, collector);
				ScoreDoc[] hits = collector.topDocs().scoreDocs;

				// 4. display results
				System.out.println("Found " + hits.length + " hits.");
				String writeToFile = "";
				for (int i = 0; i < hits.length; ++i) {
					int docId = hits[i].doc;
					Document d = searcher.doc(docId);
					//System.out.println((i + 1) + ". " + d.get("path") + " score=" + hits[i].score);
					String textSnip = textSnippetGenerator(d.get("path"));
					System.out.println((i + 1) + ". " + d.get("path") +
							" score=" + hits[i].score + " Text Snippet=" + textSnip);
					writeToFile = writeToFile + (i + 1) + ". " + d.get("path") + " score=" + hits[i].score + " Text Snippet=" + textSnip + "\n";
				}
				System.out.println("Do you wish to write the results to a file?(y=yes, any other key =no):");
				s = br.readLine();
				if (s.equalsIgnoreCase("y")) {
					System.out
					.println("Enter the FULL path(Path/folder should already exist) where you need to write the results:(e.g. /Usr/index or c:\\temp\\index)");
					String file_path = br.readLine();
					String result_file = file_path + "/" + query_text.replace(" ", "_") + "_results.txt";
					PrintWriter printWriter;
					try {
						printWriter = new PrintWriter(new FileWriter(new File(new String(result_file))));
						printWriter.write(writeToFile);
						printWriter.close();

						System.out.println("Results data successfully written to file: " + query_text.replace(" ", "_") + "_results.txt in folder you mentioned above");
					} catch (IOException e) {
						System.out.println("Exception caught. File path not found, please try again. Note: Please make sure that Path/folder already exists. Exception:" + e);
					}
				}
				s="";

				// 5. term stats --> watch out for which "version" of the term
				// must be checked here instead!
				// added this:
				String[] tokens = query_text.split(" ");
				String t = "";
				for (int i = 0; i < tokens.length; i++) {
					t = tokens[i];
					Term termInstance = new Term("contents", t);
					long termFreq = reader.totalTermFreq(termInstance);
					long docCount = reader.docFreq(termInstance);
					System.out.println("Extra Information about Query terms" + "\n" + t + " Term Frequency " + termFreq
							+ " - Document Frequency " + docCount);
				}
			} catch (Exception e) {
				System.out.println("Error searching " + s + " : "
						+ e.getMessage());
				break;
			}

		}

	}
	// Function to generate text snippet
	private static String textSnippetGenerator(String path){
		FileReader fr = null;
		System.out.println(path);
		String s = "";
		try {
			fr = new FileReader(path);
			//adding here:
			//PrintWriter printWriter = new PrintWriter(new FileWriter(new File(new String("temp.txt"))));
			BufferedReader bufferedReader = new BufferedReader(fr);
			String line;
			while((line = bufferedReader.readLine()) != null) {
				//System.out.println(line);
				s = s + line.replaceAll("\\<[^>]*>",""); 
			}   
			if(s.length() > 200) s = s.substring(0,200);
			// Close files    
			bufferedReader.close(); 
			fr.close();	

		}
		catch (IOException e) {
			System.out.println("Exception caught while trying to generate text snippet: " + e);


		}
		return s;
	}

	// function to Write Term to tf File
	private static void writeTermToTfFile(String termToTfFile, TreeMap<String, Long> sortedTermFreq){
		PrintWriter printWriter;
		try {
			printWriter = new PrintWriter(new FileWriter(new File(new String(termToTfFile))));
			for(Map.Entry<String,Long> entry : sortedTermFreq.entrySet()) {
				String term = entry.getKey();
				Long termFreq = entry.getValue();
				printWriter.write(term + " : " + termFreq + "\n");
			}	
			printWriter.close();
			System.out.println("Term to Tf data successfully written to file termToTfFile.txt in folder you mentioned above");
		} catch (IOException e) {
			System.out.println("Exception caught. File path not found, please try again. Note: Please make sure that Path/folder already exists. Exception:" + e);
		}
	}

	// function to find term frequency
	public static Boolean termToTfCalc(IndexReader reader, String file_loc){
		try {
			Fields fields = MultiFields.getFields(reader);
			Terms terms = fields.terms("contents");
			TermsEnum iterator = terms.iterator(null);
			HashMap<String, Long> termFreq_map= new HashMap<String, Long>();

			String termToTfFile = file_loc + "/termToTfFile.txt";
			PrintWriter printWriter = new PrintWriter(new FileWriter(new File(new String(termToTfFile))));

			BytesRef byteRef = null;
			while((byteRef = iterator.next()) != null) {
				String term = new String(byteRef.bytes, byteRef.offset, byteRef.length);
				Term termInstance = new Term("contents", term); 
				long termFreq = reader.totalTermFreq(termInstance);
				termFreq_map.put(term, termFreq);
			}
			TreeMap<String, Long> sortedMap = SortByValue(termFreq_map);  
			//System.out.println(sortedMap);
			writeTermToTfFile(termToTfFile, sortedMap);
			printWriter.close();
			return false; // buildList becomes #false, so it wont try to build the list again
		}
		catch (IOException e) {
			System.out.println("File path not found, please try again. Note: Please make sure that Path/folder already exists");
			return true;
		}
	}

	public static TreeMap<String, Long> SortByValue 
	(HashMap<String, Long> map) {
		ValueComparator vc =  new ValueComparator(map);
		TreeMap<String,Long> sortedMap = new TreeMap<String,Long>(vc);
		sortedMap.putAll(map);
		return sortedMap;
	}

	/**
	 * Constructor
	 * 
	 * @param indexDir
	 *            the name of the folder in which the index should be created
	 * @throws java.io.IOException
	 *             when exception creating index.
	 */
	IndexerAndRet(String indexDir) throws IOException {

		FSDirectory dir = FSDirectory.open(new File(indexDir));

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
				sAnalyzer);

		writer = new IndexWriter(dir, config);
	}

	/**
	 * Indexes a file or directory
	 * 
	 * @param fileName
	 *            the name of a text file or a folder we wish to add to the
	 *            index
	 * @throws java.io.IOException
	 *             when exception
	 */
	public void indexFileOrDirectory(String fileName) throws IOException {
		// ===================================================
		// gets the list of files in a folder (if user has submitted
		// the name of a folder) or gets a single file name (is user
		// has submitted only the file name)
		// ===================================================
		addFiles(new File(fileName));

		int originalNumDocs = writer.numDocs();
		for (File f : queue) {
			FileReader fr = null;
			try {
				Document doc = new Document();

				// ===================================================
				// add contents of file
				// ===================================================
				fr = new FileReader(f);

				PrintWriter printWriter = new PrintWriter(new FileWriter(new File(new String("temp.txt"))));
				BufferedReader bufferedReader = new BufferedReader(fr);
				String line;
				while((line = bufferedReader.readLine()) != null) {
					//System.out.println(line);
					String s = line.replaceAll("\\<[^>]*>",""); 
					printWriter.write(s + "\n");
				}   
				// Close files    
				bufferedReader.close(); 
				printWriter.close();
				fr.close();	
				fr = new FileReader("temp.txt");

				doc.add(new TextField("contents", fr));
				doc.add(new StringField("path", f.getPath(), Field.Store.YES));
				doc.add(new StringField("filename", f.getName(),
						Field.Store.YES));

				writer.addDocument(doc);
				System.out.println("Added: " + f);
			} catch (Exception e) {
				System.out.println("Could not add: " + f);
			} finally {
				fr.close();
			}
		}

		int newNumDocs = writer.numDocs();
		System.out.println("");
		System.out.println("************************");
		System.out
		.println((newNumDocs - originalNumDocs) + " documents added.");
		System.out.println("************************");

		queue.clear();
	}

	private void addFiles(File file) {

		if (!file.exists()) {
			System.out.println(file + " does not exist.");
		}
		if (file.isDirectory()) {
			for (File f : file.listFiles()) {
				addFiles(f);
			}
		} else {
			String filename = file.getName().toLowerCase();
			// ===================================================
			// Only index text files
			// ===================================================
			if (filename.endsWith(".htm") || filename.endsWith(".html")
					|| filename.endsWith(".xml") || filename.endsWith(".txt")) {
				queue.add(file);
			} else {
				System.out.println("Skipped " + filename);
			}
		}
	}

	/**
	 * Close the index.
	 * 
	 * @throws java.io.IOException
	 *             when exception closing
	 */
	public void closeIndex() throws IOException {
		writer.close();
	}
}

class ValueComparator implements Comparator<String> {

	Map<String, Long> map;

	public ValueComparator(Map<String, Long> base) {
		this.map = base;
	}

	public int compare(String a, String b) {
		if (map.get(a) >= map.get(b)) {
			return -1;
		} else {
			return 1;
		} 
	}
}