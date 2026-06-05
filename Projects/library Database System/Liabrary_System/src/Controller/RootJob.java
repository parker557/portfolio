package Controller;

import View.Oracle_Login;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;

import java.sql.ResultSet;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

public class RootJob implements Job {

    public void execute(JobExecutionContext context) throws JobExecutionException {
        {
            SimpleDateFormat format=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            String time = format.format(new Date());
            System.out.println(time+";READ BORROWING AND RESERVING RECORDS");

           // jobId= email;time;borrow   或 email;time;reserve
            if (Oracle_Login.oracleDB != null)
            {
                System.out.println("Get Borrowing Records-----------------------");
                try {
                  ResultSet rs = Oracle_Login.oracleDB.executeQuery("select * from BORROW_AND_RETURN_RECORD where ReturnTime is null ");
                  while (rs.next())
                  {
                        String BookID = rs.getString("BookID");
                        String LoginID = rs.getString("LoginID");
                        System.out.println("---------------------------------------------------------------------LoginID="+LoginID);
                        Date BorrowTime = rs.getDate("BorrowTime");
                        USER_ACCOUNT user = GetUserEntity(LoginID);
                        if (!user.LoginID.equals("")) {

                            String BookName = GetBookName(BookID);
                            //In real application, this task (to send a reminding email if there is only one week before the deadline of
                            // returning the book) should be performed after 23 days (one week before the due of borrowing)
                            //Here, to be convenient for us to do the demonstration and for you to test the project
                            //We purposely perform the task 1 minute after the borrowing,
                            //which means that after 1 minute you borrowed a book, you will receive and email reminding you to return the book
                            //Date returnTime = DelayDay(BorrowTime, 23);//in real application
                            Date returnTime = DelayMinute(BorrowTime,1);//for testing purpose
                            String borrowTimeStr = GetDateString(DelayMinute(BorrowTime,-1));
                            String returnTimeStr = GetDateString(returnTime);
                            String jobId =user.Email +";" + returnTimeStr + ";borrow";
                            // The email to remind you to return the book
                            Date now = new Date();
                            if (returnTime.getTime() > now.getTime()) {
                                if (!Oracle_Login.taskIds.contains(jobId)) {
                                    Oracle_Login.taskIds.add(jobId);
                                    String mailDescription = "";
                                    mailDescription = String.format("Hi %s:<br>", user.Nickname);
                                    mailDescription += String.format("Kindly remind you that you should return the book '%s' you have borrowed " +
                                            "in one week! <br> You can keep a book for at most one month. " +
                                            "If you fail to return it on time, your account will be deactivate automatically by the library management system.<br>" , BookName);
                                    mailDescription += "PAO YUE-KONG LIBRARY<br>";
                                    mailDescription += GetDateString(new Date()) + "<br>;";
                                    // mail subject
                                    mailDescription += "Reminder: Return the Book On Time!;";
                                    mailDescription +=   BookID +";" + LoginID +";";
                                    Oracle_Login.jobs.add(new Jobs(jobId,"SwapJob.class",returnTime,mailDescription));
                                }

                            }


                            // if an account is found not to return the book in one month, deactivate it
                            //In real application, this task (to deactivate a user who failed to return a book on time) should be performed after 30 days
                            //Here, to be convenient for us to do the demonstration and for you to test the project
                            //We purposely perform the task 2 minutes later, which means that if you borrowed a book and failed to return it in 2 minutes,
                            //your account will be deactivated and you will receive an email

                            //Date deactivateTime = DelayDay(BorrowTime,30);//for real application
                            Date deactivateTime = DelayMinute(BorrowTime,5);//for test purpose
                            returnTimeStr = GetDateString(deactivateTime);
                            jobId =user.LoginID +";" + returnTimeStr + ";resetUser";
                            // BookID;LoginID;BorrowTime
                            if (deactivateTime.getTime() > now.getTime()) {
                                if (!Oracle_Login.taskIds.contains(jobId)) {
                                    Oracle_Login.taskIds.add(jobId);
                                    String setUserDescription= String.format("%s;%s;%s",BookID,LoginID,GetDateString(BorrowTime));
                                    Oracle_Login.jobs.add(new Jobs(jobId,"UserSetJob.class",deactivateTime,setUserDescription));

                                }
                            }

                        }
                  }
                  if(rs!=null){
                      rs.close();
                  }

                }
                catch (Exception ex)
                {
                    System.out.println("An exception occurred in obtaining the borrowed book data，"+ ex.getMessage());
                }

          System.out.println("Get the reservation records------------------");
                Date now = new Date();
                try {
                    ResultSet rs = Oracle_Login.oracleDB.executeQuery("select * from RESERVED_RECORD ");
                    while (rs.next())
                    {
                        String BookID = rs.getString("BookID");
                        String LoginID = rs.getString("LoginID");
                        Date ReservedTime = rs.getDate("RESERVEDTIME");
                        Date ExpectedGetTime = rs.getDate("ExpectedGetTime");

                        //In real application, we should remind the user to pick up the book he reserved
                        //one day before the deadline, However, for simplicity of testing, we purposely set
                        //the reminding time of the reservation to be 1 minute later
                        //Date remindingTime = DelayDay(ExpectedGetTime,-1);// real application
                        Date remindingTime = DelayMinute(ReservedTime,1);// for testing purpose
                        if (remindingTime.getTime() > now.getTime()) {

                            USER_ACCOUNT user = GetUserEntity(LoginID);
                            if (!user.LoginID.equals("")) {
                                String BookName = GetBookName(BookID);
                                String returnTimeStr = GetDateString(remindingTime);
                                String jobId =user.Email +";" + returnTimeStr + ";reserve";
                                if (!Oracle_Login.taskIds.contains(jobId)) {
                                    Oracle_Login.taskIds.add(jobId);
                                    String mailDescription = "";
                                    mailDescription = String.format("Hi %s:<br>", user.Nickname);
                                    mailDescription += String.format("You have reserved the book '%s' two days ago, the deadline for picking up " +
                                            "the book is tomorrow! Please pick it up on time! Or your reservation will be cancelled automatically!<br>", BookName);
                                    mailDescription += "PAO YUE-KONG LIBRARY<br>";
                                    mailDescription += GetDateString(new Date()) + "<br>;";

                                    // mail subject
                                    mailDescription += "Reminder: Pick Up the Reserved Book On Time!;";
                                    mailDescription +=   BookID +";" + LoginID +";";
                                    Oracle_Login.jobs.add(new Jobs(jobId,"SwapJob.class",remindingTime,mailDescription));

                                }
                            }
                        }

                    }
                    if(rs!=null){
                        rs.close();
                    }
                }

                catch (Exception ex)
                {
                    System.out.println("An exception occurred in obtaining reservation data，"+ ex.getMessage());
                }
            }
            else {
                System.out.println("oracleDB2 is null,unable to get the database data");
            }

                System.out.println("-------Iterate over the existing task Id--------------------------");
           for(int i=0;i < Oracle_Login.taskIds.size();i++)
           {
               System.out.println("jobId"+ i+"="+Oracle_Login.taskIds.get(i));
           }
            System.out.println("---------------------------------");
        }


    }

    public USER_ACCOUNT GetUserEntity(String loginId)
    {
        USER_ACCOUNT entity = new USER_ACCOUNT("","","");
        try {
            ResultSet rs = Oracle_Login.oracleDB.executeQuery(String.format("select * from USER_ACCOUNT where LoginID='%s' ",loginId));
            if (rs.next())
            {
                String email = rs.getString("Email");
                String nickname = rs.getString("Nickname");
                entity = new USER_ACCOUNT(loginId,nickname,email);
            }
            if(rs!=null){
                rs.close();
            }
        }
        catch (Exception ex)
        {
            PrintLog("Fail to get the user entity，" + ex.getMessage());
        }

        return entity;
    }

    public String GetBookName(String bookId)
    {
        String name="";
        if (!bookId.equals(""))
        {
            try {
                ResultSet rs = Oracle_Login.oracleDB.executeQuery(String.format("select * from BOOK where BookID='%s' ",bookId));
                if (rs.next())
                {
                    name = rs.getString("BookName");
                }
                if(rs!=null){
                    rs.close();
                }
            }
            catch (Exception ex)
            {
                PrintLog("Failed to obtain book title，" + ex.getMessage());
            }
        }

        return name;
    }

    public void PrintLog(String msg)
    {
        System.out.println(msg);
    }

    public Date DelayDay(Date date,int delayDays)
    {
        Calendar calendar  =   Calendar.getInstance();
        calendar.setTime(date); //需要将date数据转移到Calender对象中操作
        calendar.add(calendar.DATE, delayDays);//把日期往后增加n天.正数往后推,负数往前移动
        date = calendar.getTime();

        return date;
    }

    public Date DelayMinute(Date date,int delayMinutes)
    {
        Calendar calendar  =   Calendar.getInstance();
        calendar.setTime(date); //需要将date数据转移到Calender对象中操作
        calendar.add(calendar.MINUTE, delayMinutes);//把日期往后增加n天.正数往后推,负数往前移动
        date = calendar.getTime();

        return date;
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
}
