import org.apache.lucene.document.Document;
import org.apache.lucene.analysis.core.WhitespaceAnalyzer;
import org.apache.lucene.analysis.Analyzer;

import org.apache.lucene.document.TextField;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;

import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;

import org.apache.lucene.search.IndexSearcher;

import java.io.Reader;
import java.io.UncheckedIOException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.BufferedReader;

import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.*;
import java.util.function.*;
import java.lang.*;
import java.util.Iterator;

import java.util.Collection;
import java.util.Collections;

import org.apache.lucene.store.Directory;
import org.apache.lucene.store.NIOFSDirectory;


public class Searcher {
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
    
    private static Integer searching(String source, String res_exemplar, IndexSearcher searcher, QueryParser parser) throws Exception {
        BufferedReader test_code = new BufferedReader(new FileReader(source));
        PrintWriter exemplar_res = new PrintWriter(res_exemplar, "UTF-8");
        String x;
        while ((x = test_code.readLine()) != null) {
            try {
                String escaped = escape(x.trim());
                ScoreDoc[] D = searcher.search(parser.parse(escaped), 20).scoreDocs;
                // Document doc = searcher.doc(D[0].doc);
                // exemplar_res.println(doc.get("No"));
                for (Integer i = 0; i < D.length; i++) {
                    Document doc = searcher.doc(D[i].doc);
                    exemplar_res.print(doc.get("No"));
                    exemplar_res.print(" ");
                    // exemplar_res.println(D[i].score);
                    // if (!escaped.equals(doc.get("code"))) {
                    //     exemplar_res.print(doc.get("No"));
                    //     exemplar_res.print(" ");
                    // } 
		        }
                exemplar_res.println();
            } catch (Exception e) {
                exemplar_res.println("xxx");
            }       
        } 
        exemplar_res.close();
        return 1;
    }

    /**
     * dir     test_code   exemplar
     * 0       1           2
     */
    public static void main(String[] args) throws Exception {
        for (Integer i = 0; i < args.length; ++i) {
            System.out.print(i);
            System.out.print(": ");
            System.out.println(args[i]);
        }
        Path p = FileSystems.getDefault().getPath(args[0]);
        Directory index = new NIOFSDirectory(p);
        Analyzer analyzer = new WhitespaceAnalyzer();
        IndexWriterConfig config = new IndexWriterConfig(analyzer);
        config.setOpenMode(IndexWriterConfig.OpenMode.APPEND);
        IndexWriter w = new IndexWriter(index, config);

        IndexReader r = DirectoryReader.open(w);

        IndexSearcher searcher = new IndexSearcher(r);

        QueryParser parser = new QueryParser("nl", analyzer);

        for (Integer i = 1; i < args.length; i += 2) {
            System.out.print("processing ");
            System.out.println(args[i]);
            System.out.println(searching(args[i], args[i+1], searcher, parser));
        }
    }
}
