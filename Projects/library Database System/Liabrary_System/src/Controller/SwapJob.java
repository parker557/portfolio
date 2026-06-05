package Controller;

import View.Oracle_Login;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.quartz.Trigger;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class SwapJob implements Job {

    public void execute(JobExecutionContext context) throws JobExecutionException {

        SimpleDateFormat format=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String time = format.format(new Date());


        System.out.println(time+"; Perform regular task");
        Trigger tr = context.getTrigger();
        String jobId = tr.getJobKey().toString().replace("FH_JOBGROUP_NAME.","");

        System.out.println("job Name"+ tr.getJobKey());
        System.out.println("job description="+ tr.getDescription());

        System.out.println("---------------------");

        String[] mainContentList = tr.getDescription().split(";");
        String email = tr.getJobKey().toString().replace("FH_JOBGROUP_NAME.","").split(";")[0];
       // huhai@hantek.com;122-11-14 11:33:35;borrow
        String LoginID = mainContentList[3];
        String BookId = mainContentList[2];
        boolean execute = false;
        if(jobId.split(";")[2].equals("borrow")){
            String sql = String.format("select * from BORROW_AND_RETURN_RECORD where BookID='%s' and LoginID='%s'",BookId,LoginID);
            try {
                ResultSet rset = Oracle_Login.oracleDB.executeQuery(sql);
                if(rset.next()){
                    if(rset.getDate("ReturnTime")==null){
                        execute = true;
                    }else execute =false;
                }
                if(rset!=null){
                    rset.close();
                }
            } catch (SQLException e) {
                throw new RuntimeException(e);
            }

        }else if(jobId.split(";")[2].equals("reserve")){
            String sql = String.format("select * from RESERVED_RECORD where BookID='%s' and LoginID='%s'",BookId,LoginID);
            try {
                ResultSet rset = Oracle_Login.oracleDB.executeQuery(sql);
                if(rset.next()){
                    execute = true;
                }
                else {
                    execute =false;
                }
                if(rset!=null){
                    rset.close();
                }
            } catch (SQLException e) {
                throw new RuntimeException(e);
            }
        }


        String subject = mainContentList[1];
        String mailContent = mainContentList[0];
        if(execute == true)
            new EmailControll().SendLibraryEmail(email,subject,mailContent);

    }

}
