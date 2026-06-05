package Controller;

import java.util.Date;

public class Jobs {

    public String jobId;
    public String jobType;
    public Date returnTime;
    public String mailDescription;
    public Jobs(String jobId,String jobType,Date returnTime,String mailDescription){
        this.jobId = jobId;
        this.jobType = jobType;
        this.returnTime = returnTime;
        this.mailDescription = mailDescription;
    }

    public String getJobId() {
        return jobId;
    }

    public String getJobType() {
        return jobType;
    }

    public Date getReturnTime() {
        return returnTime;
    }

    public String getMailDescription() {
        return mailDescription;
    }



}
