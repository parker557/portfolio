package Controller;

import View.Oracle_Login;

import java.sql.ResultSet;
import java.sql.SQLException;

public class BookRecordController {

    public static ResultSet searchBorrowReturn(String keyWord) throws SQLException {
        OracleDB oracleDB = Oracle_Login.oracleDB;
        String sql=" select * from (SELECT a.*, b.Nickname, b.Email,c.STATUS,c.BookName,c.AUTHOR,c.CATEGORY,c.PUBLISHER,";
        sql +=" CASE c.STATUS";
        sql +=" WHEN 0 THEN 'Available'";
        sql +=" WHEN 1 THEN 'Borrowed'";
        sql +=" WHEN 2 THEN 'Reserved'";
        sql +=" ELSE '' END";
        sql +=" As StatusName";
        sql +=" FROM BORROW_AND_RETURN_RECORD a";
        sql +=" left join USER_Account b on a.LOGINID = B.LOGINID";
        sql +=" left join book c on a.BOOKID = C.BOOKID)";
        sql +=" where BookId LIKE '%" + keyWord + "%'" ;
        sql +=" OR AUTHOR LIKE '%" + keyWord + "%'" ;
        sql +=" OR BOOKNAME LIKE '%" + keyWord + "%'" ;
        sql +=" OR PUBLISHER LIKE '%" + keyWord + "%'" ;
        sql +=" OR CATEGORY LIKE '%" + keyWord + "%'" ;

       // sql += String.format(" where BookId LIKE '%%s%' ",bookId);

        ResultSet rset = oracleDB.executeQuery(sql);
        return rset;
    }

}
