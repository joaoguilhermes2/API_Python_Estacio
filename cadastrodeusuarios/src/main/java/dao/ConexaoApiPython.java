/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package dao;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;

public class ConexaoApiPython{
    private static final String API_URL = "http://localhost:5000/register"; 
    
    public static void enviarDados(String nome, String email, String telefone, File foto) {
        String boundary = "----WebKitFormBoundary" + System.currentTimeMillis();
        
        try{
            //tenta conexao
            URL url = new URL(API_URL);
            HttpURLConnection conexao = (HttpURLConnection) url.openConnection();
            conexao.setRequestMethod("POST");
            conexao.setDoOutput(true);
            conexao.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);
            
            
            //requisicao
            try (OutputStream outputstream = conexao.getOutputStream();
                 PrintWriter writer = new PrintWriter(new OutputStreamWriter(outputstream, "UTF-8"), true)) {
            
                //adicionar campos
                addFieldText(writer, boundary, "nome", nome);
                addFieldText(writer, boundary, "email", email);
                addFieldText(writer, boundary, "telefone", telefone);
                
                //adicionar foto
                if(foto != null) {
                    addFieldArchive(writer, outputstream, boundary, "foto", foto);
                }
                
                //fim requisição
                writer.append("--").append(boundary).append("--").append("\r\n");
                writer.flush();                             
            }
            
            //resposta api
            
            int responseApi = conexao.getResponseCode();
            if(responseApi == HttpURLConnection.HTTP_OK || responseApi == HttpURLConnection.HTTP_CREATED){
                try(BufferedReader reader = new BufferedReader(new InputStreamReader(conexao.getInputStream()))){
                    String linha;
                    StringBuilder response = new StringBuilder();
                    while ((linha = reader.readLine()) != null) {
                        response.append(linha);
                    }
                   System.out.println("****Resposta API****: " + response.toString());
                }
            }else{
                    System.err.println("Erro ao enviar dados: " + conexao.getResponseMessage());
                    }  
                
            }catch (IOException e) {
                    e.printStackTrace();
                    }          
        }
    
    private static void addFieldText(PrintWriter writer, String boundary, String campo, String valor){
        writer.append("--").append(boundary).append("\r\n");
        writer.append("Content-Disposition: form-data; name=\"").append(campo).append("\"\r\n\r\n");
        writer.append(valor).append("\r\n");
        writer.flush();   
    }
    
    private static void addFieldArchive(PrintWriter writer, OutputStream outputstream, String boundary, String campo, File arquivo) throws IOException {
        if(!arquivo.exists() || !arquivo.isFile()){
            throw new IOException("Arquivo inválido ou inexistente: " + arquivo.getAbsolutePath());
        }      
            
        writer.append("--").append(boundary).append("\r\n");
        writer.append("Content-Disposition: form-data; name=\"").append(campo).append("\"; filename=\"").append(arquivo.getName()).append("\"\r\n");
        
        String contentType = Files.probeContentType(arquivo.toPath());
        
        if(contentType == null){
            contentType = "application/octet-stream";
        }
        writer.append("Content-Type: ").append(contentType).append("\r\n\r\n");
        writer.flush();
        
        //envio do arquivo
        try(FileInputStream inputStream = new FileInputStream(arquivo)) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = inputStream.read(buffer)) != -1 ) {
                outputstream.write(buffer, 0, bytesRead);
            }
            outputstream.flush();
        }
        writer.append("\r\n");
        writer.flush();
        
    }
}



/**
 *
 * @author gabri
 */
