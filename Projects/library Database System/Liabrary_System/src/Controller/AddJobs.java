package Controller;

import View.Oracle_Login;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;

import java.util.Date;
import java.util.*;
public class AddJobs implements Job {

    @Override
    public void execute(JobExecutionContext jobExecutionContext) throws JobExecutionException {


        if (Oracle_Login.jobs.size() > 0) {
            for (int i = 0; i < Oracle_Login.jobs.size(); i++) {
                String jobId = Oracle_Login.jobs.get(i).getJobId();
                String jobType = Oracle_Login.jobs.get(i).getJobType();
                Date returnTime = Oracle_Login.jobs.get(i).getReturnTime();
                String mailDescription = Oracle_Login.jobs.get(i).getMailDescription();
                if (jobType.equals("SwapJob.class")) {
                    System.out.println("----------------------Starting adding jobs----------------------");
                    QuartzManager.addJob(jobId, SwapJob.class, CronDateUtils.getCron(returnTime), mailDescription);
                    System.out.println("----------------------Successfully add a job----------------------");
                }
                else if (jobType.equals("UserSetJob.class"))
                {
                    QuartzManager.addJob(jobId, UserSetJob.class, CronDateUtils.getCron(returnTime), mailDescription);
                }
            }
            // 清空jobs
            Oracle_Login.jobs = new ArrayList<>();
        }


    }
}
