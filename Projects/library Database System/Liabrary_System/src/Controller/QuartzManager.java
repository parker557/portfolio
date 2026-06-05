package Controller;

import org.quartz.*;
import org.quartz.impl.StdSchedulerFactory;

import java.util.Map;

public class QuartzManager {
    private static SchedulerFactory gSchedulerFactory = new StdSchedulerFactory();  //Create a SchedulerFactory factory instance
    private static String JOB_GROUP_NAME = "FH_JOBGROUP_NAME";                      //task group
    private static String TRIGGER_GROUP_NAME = "FH_TRIGGERGROUP_NAME";              //trigger group

    /**Add a scheduled task using the default task group name, trigger name, trigger group name
     * @param jobName task name
     * @param cls task
     * @param time time Settings, refer to the quartz documentation
     */
    public static void addJob(String jobName, Class<? extends Job> cls, String time,String description) {
        try {
            Scheduler sched = gSchedulerFactory.getScheduler();                                          //通过SchedulerFactory构建Scheduler对象
            JobDetail jobDetail= JobBuilder.newJob(cls).withIdentity(jobName,JOB_GROUP_NAME).build();    //用于描叙Job实现类及其他的一些静态信息，构建一个作业实例
            CronTrigger trigger = (CronTrigger) TriggerBuilder
                    .newTrigger()                                                                         //创建一个新的TriggerBuilder来规范一个触发器
                    .withIdentity(jobName, TRIGGER_GROUP_NAME)                                            //给触发器起一个名字和组名
                    .withDescription(description)
                    .withSchedule(CronScheduleBuilder.cronSchedule(time))
                    .build();
            sched.scheduleJob(jobDetail, trigger);
            if (!sched.isShutdown()) {
                sched.start();        // 启动
            }
        } catch (Exception e) {
            System.out.println("add job error, " + e.getMessage());
        }
    }

    /**添加一个定时任务，使用默认的任务组名，触发器名，触发器组名  （带参数）
     * @param jobName 任务名
     * @param cls 任务
     * @param time 时间设置，参考quartz说明文档
     */
    public static void addJob(String jobName, Class<? extends Job> cls, String time, Map<String,Object> parameter) {
        try {
            Scheduler sched = gSchedulerFactory.getScheduler();                                          //通过SchedulerFactory构建Scheduler对象
            JobDetail jobDetail= JobBuilder.newJob(cls).withIdentity(jobName,JOB_GROUP_NAME).build();    //用于描叙Job实现类及其他的一些静态信息，构建一个作业实例
            jobDetail.getJobDataMap().put("parameterList", parameter);                                //传参数
            CronTrigger trigger = (CronTrigger) TriggerBuilder
                    .newTrigger()                                                                         //创建一个新的TriggerBuilder来规范一个触发器
                    .withIdentity(jobName, TRIGGER_GROUP_NAME)                                            //给触发器起一个名字和组名
                    .withSchedule(CronScheduleBuilder.cronSchedule(time))
                    .build();
            sched.scheduleJob(jobDetail, trigger);
            if (!sched.isShutdown()) {
                sched.start();        // 启动
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**添加一个定时任务
     * @param jobName    任务名
     * @param jobGroupName    任务组名
     * @param triggerName    触发器名
     * @param triggerGroupName    触发器组名
     * @param jobClass    任务
     * @param time    时间设置，参考quartz说明文档
     */
    public static void addJob(String jobName, String jobGroupName,
                              String triggerName, String triggerGroupName, Class<? extends Job> jobClass,
                              String time) {
        try {
            Scheduler sched = gSchedulerFactory.getScheduler();
            JobDetail jobDetail= JobBuilder.newJob(jobClass).withIdentity(jobName,jobGroupName).build();// 任务名，任务组，任务执行类
            CronTrigger trigger = (CronTrigger) TriggerBuilder     // 触发器
                    .newTrigger()
                    .withIdentity(triggerName, triggerGroupName)
                    .withSchedule(CronScheduleBuilder.cronSchedule(time))
                    .build();
            sched.scheduleJob(jobDetail, trigger);
            if (!sched.isShutdown()) {
                sched.start();        // 启动
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**添加一个定时任务  （带参数）
     * @param jobName    任务名
     * @param jobGroupName    任务组名
     * @param triggerName    触发器名
     * @param triggerGroupName    触发器组名
     * @param jobClass    任务
     * @param time    时间设置，参考quartz说明文档
     */
    public static void addJob(String jobName, String jobGroupName,
                              String triggerName, String triggerGroupName, Class<? extends Job> jobClass,
                              String time, Map<String,Object> parameter) {
        try {
            Scheduler sched = gSchedulerFactory.getScheduler();
            JobDetail jobDetail= JobBuilder.newJob(jobClass).withIdentity(jobName,jobGroupName).build();// 任务名，任务组，任务执行类
            jobDetail.getJobDataMap().put("parameterList", parameter);                                //传参数
            CronTrigger trigger = (CronTrigger) TriggerBuilder     // 触发器
                    .newTrigger()
                    .withIdentity(triggerName, triggerGroupName)
                    .withSchedule(CronScheduleBuilder.cronSchedule(time))
                    .build();
            sched.scheduleJob(jobDetail, trigger);
            if (!sched.isShutdown()) {
                sched.start();        // 启动
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
    /**
     * start up all jobs
     */
    public static void startJobs() {
        try {
            Scheduler sched = gSchedulerFactory.getScheduler();
            sched.start();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * shut down all jobs
     */
    public static void shutdownJobs() {
        try {
            Scheduler sched = gSchedulerFactory.getScheduler();
            if (!sched.isShutdown()) {
                sched.shutdown();
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}