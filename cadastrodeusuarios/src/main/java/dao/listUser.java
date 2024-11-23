///*
// * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
// * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
// */
//package dao;
//
//import java.sql.*;
//import java.util.ArrayList;
//import java.util.List;
//
///**
// *
// * @author gabri
// */
//public class listUser {
//    private static final String URL = "jdbc:mysql://localhost:3306/senac_cadastro";
//    private static final String USER = "root";
//    private static final String PASSWORD = "";
//    
//        public List<Usuario> listarUsuariosCadastrados(){
//            List<Usuario> usuarios = new ArrayList<>();
//            
//            string sql = "SELECT nome, email, telefone, foto FROM usuarios";
//            
//            try(Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
//                    Statement stmt = conn.createStatement();
//                    ResultSet rs = stmt.executeQuery(sql)
//                    ){
//            while (rs.next()){
//                Usuario usuario = new Usuario(
//                        rs.getString("nome"),
//                        rs.getString("email"),
//                        rs.getString("telefone"),
//                        rs.getString("foto")
//                );
//                usuarios.add(usuario);
//            }
//            }catch(SQLException e) {
//                e.printStackTrace();
//            }
//            return usuarios;
//        }
//    
//    
//}
