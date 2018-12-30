import java.sql.*;
import java.text.SimpleDateFormat;
import java.util.Date;

public class SuggestionBoxSQL {
    Connection conn = null;
    Statement stmt = null;
    String outputString = "";

    SuggestionBoxSQL(String suggestion, boolean show) {
        if (show) {
            try {
                conn = DriverManager
                        .getConnection("jdbc:mysql://localhost/suggestion_box?" + "user=root&password=12345678&useSSL=false");
                stmt = conn.createStatement();
                String sql = "SELECT postDate,msg FROM suggestion_msg";
                ResultSet rs = stmt.executeQuery(sql);
                while (rs.next()) {
                    String date = rs.getString("postDate");
                    String message = rs.getString("msg");
                    outputString += "Post Date: ";
                    outputString += date;
                    outputString += "\nMessage: ";
                    outputString += message;
                    outputString += "\n \n";
                }
                rs.close();
            } catch (SQLException ex) {
                // handle any errors
                System.out.println("SQLException: " + ex.getMessage());
                System.out.println("SQLState: " + ex.getSQLState());
                System.out.println("VendorError: " + ex.getErrorCode());
            }
        } else {
            try {
                conn = DriverManager
                        .getConnection("jdbc:mysql://localhost/suggestion_box?" + "user=root&password=12345678&useSSL=false");
                stmt = conn.createStatement();
                PreparedStatement ps = conn.prepareStatement("insert into suggestion_msg (postDate,msg) VALUES (?,?)");
                SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                ps.setString(1, df.format(new Date()));
                ps.setString(2, suggestion);
                ps.executeUpdate();
                ps.close();
            } catch (SQLException ex) {
                // handle any errors
                System.out.println("SQLException: " + ex.getMessage());
                System.out.println("SQLState: " + ex.getSQLState());
                System.out.println("VendorError: " + ex.getErrorCode());
            }
        }
    }
}
