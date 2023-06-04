import org.apache.lucene.document.Document;
import org.apache.lucene.analysis.core.WhitespaceAnalyzer;
import org.apache.lucene.analysis.Analyzer;

import org.apache.lucene.document.TextField;
import org.apache.lucene.document.StoredField;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;

import java.io.Reader;
import java.io.FileReader;
import java.io.BufferedReader;

import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.lang.*;
import java.util.Iterator;

import org.apache.lucene.store.Directory;
import org.apache.lucene.store.NIOFSDirectory;


public class IndexBuilder {
    private static String escape(String a) {
        return a
            .replace("\\", "\\\\")
            .replace("+", "\\+")
            .replace("-", "\\-")
            .replace("&", "\\&")
            .replace("|", "\\|")
            .replace("!", "\\!")
            .replace("(", "\\(")
            .replace(")", "\\)")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace("[", "\\[")
            .replace("]", "\\]")
            .replace("^", "\\^")
            .replace("\"", "\\\"")
            .replace("~", "\\~")
            .replace("*", "\\*")
            .replace("?", "\\?")
            .replace(":", "\\:")
            .replace("/", "\\/")
            .replace("OR", "aseORase")
            .replace("AND", "aseANDase")
            .replace("NOT", "aseNOTase");
    }
    
    /**
     * train_code   dir
     * 0            1
     */
    public static void main(String[] args) throws Exception {
        for (Integer i = 0; i < args.length; ++i) {
            System.out.print(i);
            System.out.print(": ");
            System.out.println(args[i]);
        }
        Path p = FileSystems.getDefault().getPath(args[1]);
        Directory index = new NIOFSDirectory(p);
        Analyzer analyzer = new WhitespaceAnalyzer();
        IndexWriterConfig config = new IndexWriterConfig(analyzer);
        IndexWriter w = new IndexWriter(index, config);

        BufferedReader train_code = new BufferedReader(new FileReader(args[0]));

        for (int i = 0; ; ++i) {
            String thisLine = train_code.readLine();
            if (thisLine == null) break;
            Document d = new Document();
            d.add(new TextField("nl", escape(thisLine.trim()), Field.Store.YES));
            d.add(new StoredField("No", i));
            w.addDocument(d);
        }
        w.commit();
    }
}
