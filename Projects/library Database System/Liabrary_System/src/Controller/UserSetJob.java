package Controller;

import View.Oracle_Login;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.quartz.Trigger;

import java.sql.ResultSet;
import java.text.SimpleDateFormat;
import java.util.Date;

public class UserSetJob implements Job {

    public void execute(JobExecutionContext context) throws JobExecutionException {

        SimpleDateFormat format=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String time = format.format(new Date());

        System.out.println(time+"; Reset the users regularly---------------------------");
        Trigger tr = context.getTrigger();
        String jobId = tr.getJobKey().toString().replace("FH_JOBGROUP_NAME.","");
        System.out.println("job Name"+ tr.getJobKey());
        System.out.println("job description="+ tr.getDescription());
        System.out.println("---------------------");

        try {
            String[] mainContentList = tr.getDescription().split(";");
            //BookID;LoginID;BorrowTime
            String BookID = mainContentList[0];
            String LoginID = mainContentList[1];
            String BorrowTime = mainContentList[2];
            SimpleDateFormat formatBorrow=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            Date date = formatBorrow.parse(BorrowTime);
            String sql = String.format("select * from BORROW_AND_RETURN_RECORD where BookID='%s' and LoginID='%s'",BookID,LoginID);
            ResultSet rs = Oracle_Login.oracleDB.executeQuery(sql);
            if (rs.next())
            {
               Date ReturnTime = rs.getDate("ReturnTime");
               if (ReturnTime == null)
               {
                   // not return the book
                   String sqlUser = String.format("update USER_ACCOUNT set AccountStatus=1 where LoginID='%s' ",LoginID);
                   int execInt = Oracle_Login.oracleDB.executeUpdate(sqlUser);
                   System.out.println("Regularly execute user sql result  = "+ execInt);
                   if (execInt > 0)
                   {
                      ResultSet userRS = Oracle_Login.oracleDB.executeQuery(String.format("select * from USER_ACCOUNT where LoginID='%s'  ",LoginID));
                        if (userRS.next()) {

                            String nickName= userRS.getString("Nickname");
                            String email=userRS.getString("Email");

                            String mailDescription = "";
                            mailDescription = String.format("Hi %s:<br>", nickName);
                            mailDescription += "Sorry to inform you that your account has been deactivated " +
                                    "because you failed to return the book on time.<br> " +
                                    "To reactivate your account, contact our administrator!<br>";
                            mailDescription += "PAO YUE-KONG LIBRARY<br>";
                            mailDescription += GetDateString(new Date()) + "<br>";
                            // mail subject
                            String subject = "Reminder: Account Deactivated!";

                            new EmailControll().SendLibraryEmail(email, subject, mailDescription);
                        }

                       closeResult(userRS);
                   }
               }
            }

            closeResult(rs);
        }
        catch (Exception ex)
        {
            System.out.println("Regularly execute User Statue job error;"+ ex.getMessage());
        }


    }

    public static String GetDateString(Date date)
    {
        return date.getYear()+"-"+(date.getMonth()+1)+"-"+date.getDate()+" "+GetHours(date)+":"+GetMinutes(date)+":"+GetSecond(date);
    }

    public static int GetHours(Date date)
    {
        int result = 0;
        try {
            result = date.getHours();
        }
        catch (Exception ex)
        {

        }

        return result;
    }

    public static int GetMinutes(Date date)
    {
        int result = 0;
        try {
            result = date.getMinutes();
        }
        catch (Exception ex)
        {

        }

        return result;
    }

    public static int GetSecond(Date date)
    {
        int result = 0;
        try {
            result = date.getSeconds();
        }
        catch (Exception ex)
        {

        }

        return result;
    }


    public void closeResult(ResultSet rs)
    {
        try {
            if (rs != null)
            {
                rs.close();
            }

        }
        catch (Exception ex)
        {
            System.out.println("close resultSet，" + ex.getMessage());
        }
    }
}
