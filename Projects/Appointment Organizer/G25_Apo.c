#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h> 
struct INITCMD {
    /* data */
    //store inputs
    char startDay[10];
    char endDay[10];
    //default size = 10，actual size = userNum
    char user[10][20];
    int userNum;
};

struct Appointment { //apo info
    char type[20];
    char caller[20];
    char date[10];
    int start_time;
    float duration;
    int numberOfCallee;
    char callees[10][20];
    char status[20]; //status of apo
    char cmd[20];
};

struct ChildrenFileBcak
{
    int accept_count;
    int time_count;
};

struct fileInput {
    char fileLine[200][100];
    int currentIndex;
    int totalLine;
};

struct fileInput input = {NULL, 0, 0};
struct Appointment appointments[200]; //array of apo
int apoID = 0;
int userid[10]; // array of each user with id
struct INITCMD initcmd; // the init command
char Ggg[2] = "25";
int fcfs_print_count = 1;
int priority_print_count = 1;
int all_print_count = 1;

int is_holiday(char date[]) {
    const char holidayMay2023[6][10] = { "20230501", "20230507", "20230514", "20230521", "20230526", "20230528" }; //hk holiday in May 2023 with format YYYYMMDD
    int numOfHoliday = 6;
    int i;
    for (i = 0; i < numOfHoliday; i++) {
        if (strcmp(date, holidayMay2023[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

//quick_sort
char partion_data(int low,int high,struct Appointment apo[])
{
	struct Appointment apoPicket = apo[low];
	
	while(low < high)
	{
		if(strcmp(apo[high].date,apoPicket.date)>=0 && low < high)
		{
			high --;
		}
		apo[low] = apo[high];
		
		if(strcmp(apo[low].date,apoPicket.date)<=0 && low < high)
		{
			low ++;
		}
		
		apo[high] = apo[low];
	}
	apo[low] = apoPicket;
	return low;
}


void quick_sort_data(int low ,int high,struct Appointment apo[])
{
	if(low < high)
	{
		int p = partion_data(low,high,apo);
		quick_sort_data(low ,p - 1,apo);
		quick_sort_data(p + 1 ,high,apo);
	}
}

char partion_time(int low,int high,struct Appointment apo[])
{
	struct Appointment apoPicket = apo[low];
	
	while(low < high)
	{
		if(apo[high].start_time >= apoPicket.start_time && low < high)
		{
			high --;
		}
		apo[low] = apo[high];
		
		if(apo[low].start_time <= apoPicket.start_time && low < high)
		{
			low ++;
		}
		
		apo[high] = apo[low];
	}
	apo[low] = apoPicket;
	return low;
}

//quick_sort
char partion_start_time(int low,int high,struct Appointment apo[])
{
	struct Appointment apoPicket = apo[low];
	
	while(low < high)
	{
		if(strcmp(apo[high].date,apoPicket.date)<=0 && low < high)
		{
			high --;
		}
		apo[low] = apo[high];
		
		if(strcmp(apo[low].date,apoPicket.date)>0 && low < high)
		{
			low ++;
		}
		
		apo[high] = apo[low];
	}
	apo[low] = apoPicket;
	return low;
}


void quick_sort_start_time(int low ,int high,struct Appointment apo[])
{
	if(low < high)
	{
		int p = partion_start_time(low,high,apo);
		quick_sort_start_time(low ,p - 1,apo);
		quick_sort_start_time(p + 1 ,high,apo);
	}
}

void sort_apo(int low ,int high,struct Appointment apo[]){
    quick_sort_start_time(low ,high,apo);
    quick_sort_data(low ,high,apo);
}


int recordApo(struct Appointment apo) {
    if (is_holiday(apo.date)) {
        printf("-> [Fail to Record]\n");
        return 0;
    }
    appointments[apoID] = apo;
    /*
    int y;
    for (y = 0;y<=apoID;y++) {
        printf("\nAPO ID:%i\n", y);
        printf("type:%s\n", appointments[y].type);
        printf("caller:%s\n", appointments[y].caller);
        printf("date:%s\n", appointments[y].date);
        printf("time:%i\n", appointments[y].start_time);
        printf("duration:%f\n", appointments[y].duration);
        int i;
        for (i = 0; i < appointments[y].numberOfCallee; i++) {
            printf("callee: %s\n", appointments[y].callees[i]);
        }
    }
    */
    apoID++;
    printf("-> [Recorded]\n");
    //save into array to-do
}

void printApo(struct Appointment appointments[100], int length, int number) {
    int y;
    for (y = 0; y < length; y++) {
        printf("\n%d APO ID:%i\n", number, y);
        printf("%d type:%s\n", number, appointments[y].type);
        printf("%d caller:%s\n", number, appointments[y].caller);
        printf("%d date:%s\n", number, appointments[y].date);
        printf("%d time:%i\n", number, appointments[y].start_time);
        printf("%d duration:%f\n", number, appointments[y].duration);
        int i;
        for (i = 0; i < appointments[y].numberOfCallee; i++) {
            printf("%d callee: %s\n", number, appointments[y].callees[i]);
        }
    }
}


void endProgram(void) { //exit the program
    exit(0);
}

int send_multiple(int parentTochildren_Fd[][2], int childrenToparent_Fd[][2], char type[], struct Appointment appointments) {
    strcpy(appointments.type, type);
    int n;
    int send_boolean = 1;
    int send_id[initcmd.userNum];
    for (int i = 0; i < initcmd.userNum; i++) {
        send_id[i] = 0;
    }
    for (int i = 0; i < initcmd.userNum; i++) {
        for (int j = 0; j < appointments.numberOfCallee; j++) {
            if (strcmp(initcmd.user[i], appointments.callees[i]) || strcmp(initcmd.user[i], appointments.caller)) {
                send_id[i] = 1;
            }

        }

    }

    for (int i = 0; i < initcmd.userNum; i++) {
        if (send_boolean == 0) break;
        //printf("i: %d\n", i);
        if (send_id[i] == 1) {
            strcpy(appointments.cmd, "askTime");
            write(parentTochildren_Fd[i][1], &appointments, sizeof(struct Appointment));
            sleep(0.5);
            char ack_buf[80];
            while ((n = read(childrenToparent_Fd[i][0], ack_buf, 80)) > 0) { // wait children ack
                ack_buf[n] = 0;
                //printf("<parent> received children %d message [%s] is of length %d\n", i + 1, ack_buf, n);
                if (strcmp(ack_buf, "false") == 0) {
                    send_boolean = 0;
                }
                break;
            }
        }

    }
    if (send_boolean == 0) return 0;
    for (int i = 0; i < initcmd.userNum; i++) {

        if (send_id[i] == 1) {
            strcpy(appointments.cmd, "recodeTime");
            write(parentTochildren_Fd[i][1], &appointments, sizeof(struct Appointment));
            sleep(0.5);
            char ack_buf[80];
            while ((n = read(childrenToparent_Fd[i][0], ack_buf, 80)) > 0) { // wait children ack
                ack_buf[n] = 0;
                //printf("<parent> received children %d message [%s] is of length %d\n", i + 1, ack_buf, n);
                break;
            }
        }

    }
    return 1;
}

void print_reject_list(int reject_index[], int reject_count, char filename[20],char algorithm[20],int is_all) {
    FILE* outfilep;
    outfilep = fopen(filename, "a");
    FILE* rejectfilep;
    rejectfilep = fopen("G25_rejected.dat", "a");
    if(is_all == 1){
        fprintf(rejectfilep, "algorithm:%s(print ALL) the time of output %d \n",algorithm,all_print_count-1);
    }else{
        if(strcmp(algorithm,"FCFS")){
            fprintf(rejectfilep, "algorithm:%s the time of output %d \n",algorithm,fcfs_print_count-1);
        }else{
            fprintf(rejectfilep, "algorithm:%s the time of output %d \n",algorithm,priority_print_count-1);
        }
    }
    
    if (outfilep == NULL) {
        printf("Error in opening output file\n");
        exit(1);
    }
    if (rejectfilep == NULL) {
        printf("Error in opening output file\n");
        exit(1);
    }
    fprintf(outfilep, "***Rejected List*** \n");
    fprintf(rejectfilep, "***Rejected List*** \n");
    //John, you have 999 appointments. 
    fprintf(outfilep, "Altogether there are %d appointments rejected.\n", reject_count);
    fprintf(rejectfilep, "Altogether there are %d appointments rejected.\n", reject_count);
    //Date         Start   End     Type             People 
    //
    fprintf(outfilep, "========================================================================= \n");
    fprintf(rejectfilep,"========================================================================= \n");
    //2023-04-04   19:00   23:00   Gathering        Mary Paul 
    for (int i = 0; i < reject_count; i++)
    {
        //1. gathering lucy 20230414 1900 1.0 mary 
        int index = reject_index[i];
        fprintf(outfilep, "%d. %s %s %s %d %.1f ", i + 1, appointments[index].type, appointments[index].caller, appointments[index].date, appointments[index].start_time, appointments[index].duration);
        fprintf(rejectfilep, "%d. %s %s %s %d %.1f ", i + 1, appointments[index].type, appointments[index].caller, appointments[index].date, appointments[index].start_time, appointments[index].duration);
        for (int j = 0; j < appointments[index].numberOfCallee; j++)
        {
            fprintf(outfilep, " %s ", appointments[index].callees[j]);
            fprintf(rejectfilep, " %s ", appointments[index].callees[j]);
        }
        fprintf(outfilep, "\n");
        fprintf(rejectfilep, "\n");
    }
    fprintf(outfilep, "                    - End of Rejected List -  \n");
    fprintf(outfilep, "========================================================================= \n");
    fprintf(outfilep, " \n");
    fprintf(outfilep, " \n");
    fprintf(rejectfilep, "                    - End of Rejected List -  \n");
    fprintf(rejectfilep, "========================================================================= \n");
    fprintf(rejectfilep, " \n");
    fprintf(rejectfilep, " \n");
    fclose(outfilep);
    fclose(rejectfilep);
}

void write_to__children_file(int parentTochildren_Fd[][2], int childrenToparent_Fd[][2], char filename[20], int request_accept[],int children_time_count[]) {
    struct Appointment appo;
    ;
    strcpy(appo.type, filename);
    strcpy(appo.cmd, "writeFile");
    for (int i = 0; i < initcmd.userNum; i++) {
        //printf(" %d : write file\n", i + 1);
        write(parentTochildren_Fd[i][1], &appo, sizeof(struct Appointment));
        sleep(0.5);
        struct ChildrenFileBcak childBack;
        //char ack_buf[80];
        int n;
        while ((n = read(childrenToparent_Fd[i][0], &childBack, sizeof(struct ChildrenFileBcak))) > 0) { // wait children ack
            //ack_buf[n] = 0;
            request_accept[i] = childBack.accept_count;
            children_time_count[i] = childBack.time_count;
            //printf("<parent> received children %d message  is of length %d\n", i + 1, n);
            break;
        }
    }
}

void print_file_title(char algorithm[], char filename[20]) {
    FILE* outfilep;
    int  err;
    outfilep = fopen(filename, "a");
    fprintf(outfilep, "Algorithm used:  %s\n", algorithm);
    fprintf(outfilep, " \n");
    fprintf(outfilep, "***Appointment Schedule*** \n");
    fprintf(outfilep, " \n");
    fclose(outfilep);
}

void remove_same_name_file(char filename[20]) {
    FILE* outfilep;
    int  err;
    outfilep = fopen(filename, "w");
    char min_date[10];
    strcpy(min_date, initcmd.startDay);
    char max_date[10];
    strcpy(max_date, initcmd.endDay);
    /*
    for (int i = 0; i < apoID; i++)
    {
        if (strcmp(appointments[i].date, min_date) < 0) {
                strcpy(min_date, appointments[i].date);
         }
         if (strcmp(appointments[i].date, min_date) > 0) {
                strcpy(max_date, appointments[i].date);
         }
    }*/
    char year[10];
    char month[3];
    char day[3];
    strcpy(year,min_date); 
    year[4] = 0;
    month[0] = min_date[4];
    month[1] = min_date[5];
    month[2] = '\0';
    day[0] = min_date[6];
    day[1] = min_date[7];
    day[2] = '\0';
    fprintf(outfilep, "Period:%s-%s-%s to  ", year, month, day);
    strcpy(year,max_date); 
    year[5] = '\0';
    month[0] = max_date[4];
    month[1] = max_date[5];
    month[2] = '\0';
    day[0] = max_date[6];
    day[1] = max_date[7];
    day[2] = '\0';
    fprintf(outfilep, "%s-%s-%s\n", year, month, day);
    fclose(outfilep);
}

void print_performance(char filename[20], int reject_count, int request_accept[],int children_time_count[]) {
    int all_time = (initcmd.endDay[6] - initcmd.startDay[6])*10 + initcmd.endDay[7] - initcmd.startDay[7];
    all_time = all_time * 5;
    FILE* outfilep;
    int  err;
    outfilep = fopen(filename, "a");
    fprintf(outfilep, "*** Performance *** \n");
    fprintf(outfilep, " \n");
    fprintf(outfilep, "Total Number of Requests Received: %d (100.0%%)\n", apoID);
    fprintf(outfilep, "      Number of Requests Accepted: %d (%2.2f)\n", apoID - reject_count, (apoID - reject_count) * 100.0 / apoID);
    fprintf(outfilep, "      Number of Requests Rejected: %d (%2.2f)\n", reject_count, reject_count * 100.0 / apoID);
    fprintf(outfilep, " \n");
    fprintf(outfilep, "Number of Requests Accepted by Individual:  \n");
    fprintf(outfilep, " \n");
    for (int i = 0; i < initcmd.userNum; i++) {
        fprintf(outfilep, "      %s          - %d \n", initcmd.user[i], request_accept[i]);
    }                      
    fprintf(outfilep, " \n");
    fprintf(outfilep, "Utilization of Time Slot::  \n");
    fprintf(outfilep, " \n");
    for (int i = 0; i < initcmd.userNum; i++) {
        fprintf(outfilep, "      %s          - %2.2f%% \n", initcmd.user[i], children_time_count[i]*100.0/all_time);
    }                      
    fprintf(outfilep, " \n");
    fclose(outfilep);
}

void FCFSalgorithm(int parentTochildren_Fd[][2], int childrenToparent_Fd[][2], char filename[20],int is_all) {
    if( is_all == 0){
        remove_same_name_file(filename);
    }
    print_file_title("FCFS", filename);
    int reject_index[apoID];
    int reject_count = 0;
    int request_accept[initcmd.userNum];
    int children_time_count[initcmd.userNum];
    for (int i = 0; i < apoID; i++)
    {
        char caller[20];
        if (strcmp(appointments[i].type, "privateTime") == 0) {
            strcpy(caller, appointments[i].caller);
            int send_index;
            for (int j = 0; j < initcmd.userNum; j++) {
                if (strcmp(initcmd.user[j], appointments[i].caller) == 0) {
                    send_index = j;
                    break;
                }
                //write(parentTochildren_Fd[i][1],send_buf,n); // send the  string
            }
            strcpy(appointments[i].cmd, "askTime");
            write(parentTochildren_Fd[send_index][1], &appointments[i], sizeof(struct Appointment));
            sleep(0.5);
            char ack_buf[80];
            int n;
            while ((n = read(childrenToparent_Fd[send_index][0], ack_buf, 80)) > 0) { // wait children ack
                ack_buf[n] = 0;
                //printf("<parent> received children %d message [%s] is of length %d\n", send_index + 1, ack_buf, n);
                if (strcmp(ack_buf, "true") == 0) {
                    strcpy(appointments[i].cmd, "recodeTime");
                    write(parentTochildren_Fd[send_index][1], &appointments[i], sizeof(struct Appointment));
                    while ((n = read(childrenToparent_Fd[send_index][0], ack_buf, 80)) > 0) {
                        ack_buf[n] = 0;
                        //printf("<parent> received children %d message [%s] is of length %d\n", send_index + 1, ack_buf, n);
                        break;
                    }
                }
                else {
                    reject_index[reject_count] = i;
                    reject_count++;
                }
                break;
            }
        }
        else if (strcmp(appointments[i].type, "projectMeeting") == 0) {
            int schedule_result = send_multiple(parentTochildren_Fd, childrenToparent_Fd, "projectMeeting", appointments[i]);
            if (schedule_result == 0) {
                reject_index[reject_count] = i;
                reject_count++;
            }
        }
        else if (strcmp(appointments[i].type, "groupStudy") == 0) {
            int schedule_result = send_multiple(parentTochildren_Fd, childrenToparent_Fd, "groupStudy", appointments[i]);
            if (schedule_result == 0) {
                reject_index[reject_count] = i;
                reject_count++;
            }
        }
        else if (strcmp(appointments[i].type, "gathering") == 0) {
            int schedule_result = send_multiple(parentTochildren_Fd, childrenToparent_Fd, "gathering", appointments[i]);
            if (schedule_result == 0) {
                reject_index[reject_count] = i;
                reject_count++;
            }
        }
    }
    write_to__children_file(parentTochildren_Fd, childrenToparent_Fd, filename, request_accept,children_time_count);
    print_reject_list(reject_index, reject_count, filename,"FCFS",is_all);
    print_performance(filename, reject_count, request_accept,children_time_count);
}

void PriorityAlgorithm(int parentTochildren_Fd[][2], int childrenToparent_Fd[][2], char filename[20],int is_all) {
    if( is_all == 0){
        remove_same_name_file(filename);
    }
    print_file_title("Priority", filename);
    int reject_index[apoID];
    int reject_count = 0;
    int request_accept[initcmd.userNum];
    struct Appointment privateTimeApo[200]; //highest
    struct Appointment projectMeetingApo[200];
    struct Appointment groupStudyApo[200];
    struct Appointment gatheringApo[200]; //lowest
    int apoInedex[4][200];
    int ptSize = 0, pmSize = 0, gsSize = 0, gSize = 0;
    int children_time_count[initcmd.userNum];

    for (int i = 0; i < apoID; i++) {
        if (strcmp(appointments[i].type, "privateTime") == 0) {
            privateTimeApo[ptSize] = appointments[i];
            apoInedex[0][ptSize] = i;
            ptSize++;
        }
        else if (strcmp(appointments[i].type, "projectMeeting") == 0) {
            projectMeetingApo[pmSize] = appointments[i];
            apoInedex[1][pmSize] = i;
            pmSize++;
        }
        else if (strcmp(appointments[i].type, "groupStudy") == 0) {
            groupStudyApo[gsSize] = appointments[i];
            apoInedex[2][gsSize] = i;
            gsSize++;
        }
        else if (strcmp(appointments[i].type, "gathering") == 0) {
            gatheringApo[gSize] = appointments[i];
            apoInedex[3][gSize] = i;
            gSize++;
        }
        else {
            return ;  // Invalid appointment type
        }
    }
    for (int i = 0; i < ptSize; i++) {//privateTime
        char caller[20];
        strcpy(caller, privateTimeApo[i].caller);
        int send_index;
        for (int j = 0; j < initcmd.userNum; j++) {
            if (strcmp(initcmd.user[j], privateTimeApo[i].caller) == 0) {
                send_index = j;
                break;
            }
            //write(parentTochildren_Fd[i][1],send_buf,n); // send the  string
        }
        strcpy(privateTimeApo[i].cmd, "askTime");
        write(parentTochildren_Fd[send_index][1], &privateTimeApo[i], sizeof(struct Appointment));
        sleep(0.5);
        char ack_buf[80];
        int n;
        while ((n = read(childrenToparent_Fd[send_index][0], ack_buf, 80)) > 0) { // wait children ack
            ack_buf[n] = 0;
            //printf("<parent> received children %d message [%s] is of length %d\n", send_index + 1, ack_buf, n);
            if (strcmp(ack_buf, "true") == 0) {
                strcpy(privateTimeApo[i].cmd, "recodeTime");
                write(parentTochildren_Fd[send_index][1], &privateTimeApo[i], sizeof(struct Appointment));
                while ((n = read(childrenToparent_Fd[send_index][0], ack_buf, 80)) > 0) {
                    ack_buf[n] = 0;
                    //printf("<parent> received children %d message [%s] is of length %d\n", send_index + 1, ack_buf, n);
                    break;
                }
            }
            else {
                reject_index[reject_count] = apoInedex[0][i];
                reject_count++;
            }
            break;
        }
    }
    for (int i = 0; i < pmSize; i++) {//projectMeeting
        int schedule_result = send_multiple(parentTochildren_Fd, childrenToparent_Fd, "projectMeeting", projectMeetingApo[i]);
        if (schedule_result == 0) {
            reject_index[reject_count] = apoInedex[1][i];
            reject_count++;
        }
    }
    for (int i = 0; i < gsSize; i++) {//groupStudy
        int schedule_result = send_multiple(parentTochildren_Fd, childrenToparent_Fd, "groupStudy", groupStudyApo[i]);
        if (schedule_result == 0) {
            reject_index[reject_count] = apoInedex[2][i];
            reject_count++;
        }
    }
    for (int i = 0; i < gSize; i++) {//gathering
        int schedule_result = send_multiple(parentTochildren_Fd, childrenToparent_Fd, "gathering", gatheringApo[i]);
        if (schedule_result == 0) {
            reject_index[reject_count] = apoInedex[3][i];
            reject_count++;
        }
    }
    write_to__children_file(parentTochildren_Fd, childrenToparent_Fd, filename, request_accept,children_time_count);
    print_reject_list(reject_index, reject_count, filename,"PRIORITY",is_all);
    print_performance(filename, reject_count, request_accept,children_time_count);
}

char* Int2String(int num, char* str)
{
    int i = 0;
    if (num < 0)
    {
        num = -num;
        str[i++] = '-';
    }
    do
    {
        str[i++] = num % 10 + 48;
        num /= 10;
    } while (num);
    str[i] = '\0';
    int j = 0;
    if (str[0] == '-')
    {
        j = 1;
        ++i;
    }
    for (; j < i / 2; j++)
    {
        str[j] = str[j] + str[i - 1 - j];
        str[i - 1 - j] = str[j] - str[i - 1 - j];
        str[j] = str[j] - str[i - 1 - j];
    }

    return str;
}

struct Appointment readUserInput(char userInput[100]) {
    //char userInput[60];
    //printf("Please enter appointment:\n");
    //fgets(userInput, sizeof(userInput), stdin); //read user input
    
    char* type = strtok(userInput, " ");//1st input
    struct Appointment apo;
    //check command
    if (strcmp(type, "printSchd") == 0) {
        strcpy(apo.cmd, type);
        char algorithm[10];
        strcpy(algorithm, strtok(NULL, " "));//2nd input
        strcpy(apo.type, algorithm);

    }
    else if (strcmp(type, "fileInput") == 0) {
        char* filename = strtok(NULL, " "); //2nd input
        FILE* fileOpen;
        fileOpen = fopen(filename, "r");

        char buffer[100];
        while (fgets(buffer, 100, fileOpen)) {
            size_t len = strlen(buffer);
            if (len > 0 && buffer[len - 1] == '\n') {
                buffer[--len] = 0;
            }
            strcpy(input.fileLine[input.totalLine], buffer);
            input.totalLine = input.totalLine + 1;
        }
        strcpy(buffer, input.fileLine[input.currentIndex]);
        apo = readUserInput(buffer);
        input.currentIndex = input.currentIndex + 1;
        fclose(fileOpen);
    }
    else if (strcmp(type, "endProgram") == 0) {
        strcpy(apo.cmd, type);
        strcpy(apo.type, "endProgram"); // if type == endProgram, to notify the parent break the loop
    }
    else if (strcmp(type, "privateTime") == 0) {
        strcpy(apo.cmd, type);
        strcpy(apo.type, "privateTime");
        strcpy(apo.caller, strtok(NULL, " "));//2nd input
        strcpy(apo.date, strtok(NULL, " "));//3rd input
        apo.start_time = atoi(strtok(NULL, " "));//4th input cast start_time to int
        apo.duration = atof(strtok(NULL, " ")); //5th input cast duration to float
        apo.numberOfCallee = 0; //privateTime only for caller
        recordApo(apo);
    }
    else if (strcmp(type, "projectMeeting") == 0) {
        strcpy(apo.cmd, type);
        strcpy(apo.type, "projectMeeting");
        strcpy(apo.caller, strtok(NULL, " "));//2nd input
        strcpy(apo.date, strtok(NULL, " "));//3rd input
        apo.start_time = atoi(strtok(NULL, " "));//4th input cast start_time to int
        apo.duration = atof(strtok(NULL, " ")); //5th input cast duration to float
        int i = 0;
        char* token = strtok(NULL, " ");
        while (token != NULL) {
            strcpy(apo.callees[i], token);
            token = strtok(NULL, " ");
            i++;
        }
        apo.numberOfCallee = i;
        recordApo(apo);
    }
    else if (strcmp(type, "groupStudy") == 0) {
        strcpy(apo.cmd, type);
        strcpy(apo.type, "groupStudy");
        strcpy(apo.caller, strtok(NULL, " "));//2nd input
        strcpy(apo.date, strtok(NULL, " "));//3rd input
        apo.start_time = atoi(strtok(NULL, " "));//4th input cast start_time to int
        apo.duration = atof(strtok(NULL, " ")); //5th input cast duration to float
        int i = 0;
        char* token = strtok(NULL, " ");
        while (token != NULL) {
            strcpy(apo.callees[i], token);
            token = strtok(NULL, " ");
            i++;
        }
        apo.numberOfCallee = i;
        recordApo(apo);
    }
    else if (strcmp(type, "gathering") == 0) {
        strcpy(apo.cmd, type);
        strcpy(apo.type, "gathering");
        strcpy(apo.caller, strtok(NULL, " "));//2nd input
        strcpy(apo.date, strtok(NULL, " "));//3rd input
        apo.start_time = atoi(strtok(NULL, " "));//4th input cast start_time to int
        apo.duration = atof(strtok(NULL, " ")); //5th input cast duration to float
        int i = 0;
        char* token = strtok(NULL, " ");
        while (token != NULL) {
            strcpy(apo.callees[i], token);
            token = strtok(NULL, " ");
            i++;
        }
        apo.numberOfCallee = i;
        recordApo(apo);

    }
    else {
        printf("Please enter a command!\n");
        strcpy(apo.cmd, "null");
    }
    if (is_holiday(apo.date)) {
        strcpy(apo.cmd, "holiday");
    }
    return apo;
}

void init_reject_file(){
    FILE* rejectfilep;
    rejectfilep = fopen("G25_rejected.dat", "w");
    fclose(rejectfilep);

}

int main(int argc, char* argv[])
{
    /*process inputs：
    ./apo 20230401 20230430 john mary lucy paul
    argc = number of parameters, there are 7 parameters above, argc=7
    *argv[] ：every parameters，argv[1] = 20230401,argv[3] = john
    */
    printf("~~WELCOME TO APO~~ \n");

    //strcpy equalivant to initcmd.startTime=argv[1]
    strcpy(initcmd.startDay, argv[1]);
    strcpy(initcmd.endDay, argv[2]);
    initcmd.userNum = argc - 3;
    int startlen = strlen(initcmd.startDay);
    int endlen = strlen(initcmd.endDay);
    // check time
    if (startlen != 8 || endlen != 8)
    {
        perror("the time is not right\n");
        return -1;
    }
    // if user  if the number of users is out of range (not between 3 and 10)
    if (initcmd.userNum < 3 || initcmd.userNum >10)
    {
        perror("the number of users is out of range、\n");
        return -1;
    }

    //traverse names,for instance there are john mary lucy paul, i start from 3，then the first loop: initcmd.user[0] = argv[3](john),keep traversing
    int i;
    for (i = 3; i < argc; i++) {
        strcpy(initcmd.user[i - 3], argv[i]);
    }
    /*
    printf("start time: %s  end time:%s\n", initcmd.startTime, initcmd.endTime);
    */
    printf("%d users:\n", initcmd.userNum);
    //create multiple child processes. Template：https://blog.csdn.net/weixin_47397155/article/details/116568404
    int pid;
    int id = 0;
    /* create pipe */
    int parentTochildren_Fd[initcmd.userNum][2];
    int childrenToparent_Fd[initcmd.userNum][2];
    for (int i = 0; i < initcmd.userNum; i++)
    {
        if (pipe(parentTochildren_Fd[i]) < 0) {
            printf("ParentTochildren Pipe creation error\n");
            exit(1);
        }
    }
    for (int i = 0; i < initcmd.userNum; i++)
    {
        if (pipe(childrenToparent_Fd[i]) < 0) {
            printf("ChildrenToparent= Pipe creation error\n");
            exit(1);
        }
    }

    for (id = 0; id < initcmd.userNum; id++)
    {
        pid = fork();
        if (0 == pid) {
            //printf("children, pid %d ,No %d: User %s create successfully \n", getpid(), id + 1, initcmd.user[id]);
            break;//child process = jump
        }
        else if (pid > 0) {
            userid[id] = pid;
        }
    }
    if (id < initcmd.userNum) { //when the for loop over: the parent id =childnum , the children id <childnum
        char buf[80];
        int  n;
        close(parentTochildren_Fd[id][1]); // close parentTochildren write
        close(childrenToparent_Fd[id][0]); // close parentTochildren read
        struct Appointment childApo;
        struct Appointment childApoArr[100]; //array of apo
        struct Appointment myTimeTab[100];
        int timetabLength = 0;
        int apoIndex = 0;
        //read(fd,&childApo,sizeof(struct Appointment));
        //while ((n = read(parentTochildren_Fd[id][0],buf,80)) > 0) { // read from pipe
        while ((n = read(parentTochildren_Fd[id][0], &childApo, sizeof(struct Appointment))) > 0) { // read from pipe
            //buf[n] = 0;
            if (strcmp(childApo.cmd, "endProgram") == 0) {
                break;
            }
            else if (strcmp(childApo.cmd, "askTime") == 0) {
                int target_startTime = childApo.start_time;
                int target_endTime = target_startTime + childApo.duration * 100;
                int available = 1;
                for (int i = 0; i < timetabLength; i++) {
                    if (strcmp(childApo.date, myTimeTab[i].date) != 0) continue;
                    int startTime = myTimeTab[i].start_time;
                    int endTime = myTimeTab[i].start_time + myTimeTab[i].duration * 100;
                    if (!(target_endTime < startTime || endTime < target_startTime)) {
                        available = 0;
                        break;
                    }
                }
                //printf("children, pid %d ,No %d: User %s  message [%s] caller [%s] of size %d bytes received \n", getpid(), id + 1, initcmd.user[id], childApo.type, childApo.caller, n);
                char ack_buf[80];
                if (available == 1) {
                    strcpy(ack_buf, "true");
                    write(childrenToparent_Fd[id][1], ack_buf, 4);
                }
                else {
                    strcpy(ack_buf, "false");
                    write(childrenToparent_Fd[id][1], ack_buf, 5);
                }
            }
            else if (strcmp(childApo.cmd, "recodeTime") == 0)
            {
                strcpy(myTimeTab[timetabLength].type, childApo.type);
                strcpy(myTimeTab[timetabLength].date, childApo.date);
                myTimeTab[timetabLength].start_time = childApo.start_time;
                myTimeTab[timetabLength].duration = childApo.duration;
                myTimeTab[timetabLength].numberOfCallee = childApo.numberOfCallee;
                int callee_id[initcmd.userNum];
                for (int i = 0; i < initcmd.userNum; i++) {
                    callee_id[i] = 0;
                }
                for (int i = 0; i < initcmd.userNum; i++) {
                    for (int j = 0; j < childApo.numberOfCallee; j++) {
                        if (strcmp(initcmd.user[i], childApo.callees[j])) {
                            callee_id[i] = 1;
                        }
                    }
                }
                callee_id[id] = 0;
                int callees_count = 0;
                for (int i = 0; i < initcmd.userNum; i++) {
                    if (callee_id[i] == 1) {
                        strcpy(myTimeTab[timetabLength].callees[callees_count], initcmd.user[i]);
                        callees_count++;
                    }
                }

                timetabLength++;
                char ack_buf[80];
                strcpy(ack_buf, "success");
                write(childrenToparent_Fd[id][1], ack_buf, 7);

            }else if (strcmp(childApo.cmd, "writeFile") == 0) {
                struct ChildrenFileBcak fileBack;
                fileBack.accept_count = timetabLength;
                fileBack.time_count = 0;
                FILE* outfilep;
                int  err;
                outfilep = fopen(childApo.type, "a");
                if (outfilep == NULL) {
                    printf("Error in opening output file\n");
                    exit(1);
                }
                sort_apo(0,timetabLength-1,myTimeTab);
                //John, you have 999 appointments. 
                fprintf(outfilep, "%s, you have %d appointments.\n", initcmd.user[id], timetabLength);
                //Date         Start   End     Type             People 
                fprintf(outfilep, "Date\t\tStart\tEnd\t\tType\t\tPeople \n");
                //
                fprintf(outfilep, "========================================================================= \n");
                //2023-04-04   19:00   23:00   Gathering        Mary Paul 
                for (int i = 0; i < timetabLength; i++)
                {
                    int end_time = myTimeTab[i].start_time+myTimeTab[i].duration*100;
                    fileBack.time_count += myTimeTab[i].duration;
                    if(strcmp(myTimeTab[i].type,"projectMeeting") == 0){
                        fprintf(outfilep, "%s\t%d:00\t%d:00\t%s\t\t", myTimeTab[i].date, myTimeTab[i].start_time / 100,  end_time/ 100, myTimeTab[i].type);
                    }else{
                        fprintf(outfilep, "%s\t%d:00\t%d:00\t\t%s\t\t", myTimeTab[i].date, myTimeTab[i].start_time / 100,  end_time/ 100, myTimeTab[i].type);
                    }
                    
                    for (int j = 0; j < myTimeTab[i].numberOfCallee; j++)
                    {
                        //printf("numberOfCallee %d", myTimeTab[i].numberOfCallee);
                        fprintf(outfilep, "%s ", myTimeTab[i].callees[j]);
                    }
                    fprintf(outfilep, "\n");
                }
                fprintf(outfilep, "                    - End of %s's Schedule -  \n", initcmd.user[id]);
                fprintf(outfilep, "========================================================================= \n");
                fprintf(outfilep, " \n");
                fprintf(outfilep, " \n");
                fclose(outfilep);
                char ack_buf[80];
                
                //Int2String(timetabLength, ack_buf);
                //strcpy(ack_buf,"write");
                write(childrenToparent_Fd[id][1], &fileBack, sizeof(struct ChildrenFileBcak));
                timetabLength = 0;
            }
            else {
                strcpy(childApoArr[apoIndex].type, childApo.type);
                strcpy(childApoArr[apoIndex].caller, childApo.caller);//2nd input
                strcpy(childApoArr[apoIndex].date, childApo.date);//3rd input
                childApoArr[apoIndex].start_time = childApo.start_time;//4th input cast start_time to int
                childApoArr[apoIndex].duration = childApo.duration; //5th input cast duration to float
                childApoArr[apoIndex].numberOfCallee = childApo.numberOfCallee; //privateTime only for caller
                for (int i = 0; i < childApo.numberOfCallee; i++)
                {
                    strcpy(childApoArr[apoIndex].callees[i], childApo.callees[i]);
                    strcpy(childApoArr[apoIndex].callees[i], childApo.callees[i]);
                }
                apoIndex++;
                //printf("children, pid %d ,No %d: User %s  message [%s] callee [%s] of size %d bytes received \n", getpid(), id + 1, initcmd.user[id], childApo.type, childApo.caller, n);
                //printApo(childApoArr,apoIndex,id+1);
                char ack_buf[80] = "get";
                ack_buf[3] = '0';
                write(childrenToparent_Fd[id][1], ack_buf, 3);
            }
        }
        close(parentTochildren_Fd[id][0]);
        close(childrenToparent_Fd[id][1]);
        //printf("children, pid %d ,No %d: User %s completed execution \n", getpid(), id + 1, initcmd.user[id]);
        exit(0);
    }
    else {// parent process 
        // parent proccess can only quit when all child processes are exited，Template: https://www.cnblogs.com/goodcitizen/p/11133705.html
        for (int i = 0; i < initcmd.userNum; i++) {
            close(parentTochildren_Fd[i][0]); // close parentTochildren read
            close(childrenToparent_Fd[i][1]); // close childrenToparent wirte
        }
        char userInput[100];
        int n;
        FILE* logfilep;
        int  err;
        logfilep = fopen("All_Requests.dat", "w");
        init_reject_file();
        //fprintf(logfilep, "All_Requests \n");
        if (logfilep == NULL) {
            printf("Error in opening output file\n");
            exit(1);
        }
        while (1) {
            sleep(0.5);
            if (input.currentIndex == 0) {
                printf("Please enter appointment:\n");
                strcpy(userInput, "");
                n = read(STDIN_FILENO, userInput, 100); // read a line
                if (n <= 0) break; // EOF or error
                userInput[--n] = 0;
            }

            if (input.currentIndex > 0) {
                //printf("fileInput line:%d, content:%s\n", input.currentIndex, input.fileLine[input.currentIndex]);
                if (input.currentIndex == 1) {//print the request in index 0 to file
                    fprintf(logfilep, "%s \n", input.fileLine[0]);
                }
                strcpy(userInput, input.fileLine[input.currentIndex]);
                input.currentIndex = input.currentIndex + 1;
                if (input.currentIndex == input.totalLine) {//all the line been read
                    input.currentIndex = 0;
                    input.totalLine = 0;
                }
            }
            char send_buf[100];
            strcpy(send_buf, userInput);
            fprintf(logfilep, "%s \n", send_buf);

            struct Appointment apo = readUserInput(userInput); //handle the curent input
            if (strcmp(apo.cmd, "null") == 0) continue;
            //printf("<parent> message [%s] is of length %d\n",send_buf,n);
            if (strcmp(apo.cmd, "endProgram") == 0) {
                for (int i = 0; i < initcmd.userNum; i++) {
                    write(parentTochildren_Fd[i][1], &apo, sizeof(struct Appointment)); // send the  string
                }
                sleep(0.5);
                for (int i = 0; i < initcmd.userNum; i++) {
                    char ack_buf[80];
                    while ((n = read(childrenToparent_Fd[i][0], ack_buf, 80)) > 0) { // wait children ack
                        ack_buf[n] = 0;
                        //printf("<parent> received children %d message [%s] is of length %d\n", i + 1, ack_buf, n);
                        break;
                    }
                }
                break;
            }
            else if (strcmp(apo.cmd, "holiday") == 0) {
                printf("You can not make appointment on Sunday or Public holiday, Please enter again; date:\n");
                continue;
            }
            else if (strcmp(apo.cmd, "printSchd") == 0) {
                if (strcmp(apo.type, "FCFS") == 0) {
                    char fileName[20] = "G25_01_FCFS.txt";
                    if (fcfs_print_count >= 10) {
                        fileName[4] = fcfs_print_count / 10 + '0';
                    }
                    else {
                        fileName[4] = '0';
                    }
                    fileName[5] = fcfs_print_count % 10 + '0';
                    fcfs_print_count++;
                    FCFSalgorithm(parentTochildren_Fd, childrenToparent_Fd, fileName,0);
                    printf("-> [Exported file: %s] \n",fileName);
                }
                else if (strcmp(apo.type, "PRIORITY") == 0) {
                    char fileName[20] = "G25_01_Priority.txt";
                    if (priority_print_count >= 10) {
                        fileName[4] = priority_print_count / 10 + '0';
                    }
                    else {
                        fileName[4] = '0';
                    }
                    fileName[5] = priority_print_count % 10 + '0';
                    priority_print_count++;
                    PriorityAlgorithm(parentTochildren_Fd, childrenToparent_Fd, fileName,0);
                    printf("-> [Exported file: %s] \n",fileName);
                }else if (strcmp(apo.type, "ALL") == 0) {
                    char fileName[20] = "G25_01_ALL.txt";
                    if (all_print_count >= 10) {
                        fileName[4] = all_print_count / 10 + '0';
                    }
                    else {
                        fileName[4] = '0';
                    }
                    fileName[5] = all_print_count % 10 + '0';
                    all_print_count++;
                    remove_same_name_file(fileName);
                    FCFSalgorithm(parentTochildren_Fd, childrenToparent_Fd, fileName,1);
                    PriorityAlgorithm(parentTochildren_Fd, childrenToparent_Fd, fileName,1);
                    printf("-> [Exported file: %s] \n",fileName);
                }
            }
            else {
                //printf("<parent> sending  message [%s] to child\n", send_buf);
                int send_index;
                for (int i = 0; i < initcmd.userNum; i++) {
                    if (strcmp(initcmd.user[i], apo.caller) == 0) {
                        send_index = i;
                        break;
                    }
                    //write(parentTochildren_Fd[i][1],send_buf,n); // send the  string
                }
                write(parentTochildren_Fd[send_index][1], &apo, sizeof(struct Appointment));
                sleep(0.5);
                char ack_buf[80];
                while ((n = read(childrenToparent_Fd[send_index][0], ack_buf, 80)) > 0) { // wait children ack
                    ack_buf[n] = 0;
                    //printf("<parent> received children %d message [%s] is of length %d\n", send_index + 1, ack_buf, n);
                    break;
                }
            }
        }
        fclose(logfilep);
        for (int i = 0; i < initcmd.userNum; i++) {
            close(parentTochildren_Fd[i][1]); // close parent in
            close(childrenToparent_Fd[i][0]); // close parent in
        }
        int status = 0;
        int waitPid;
        for (int i = 0; i < initcmd.userNum; i++)
        {
            if ((waitPid = wait(&status)) < 0) // The waitPid means the id num of children 
                perror("wait error");
            int j;
            for (j = 0; j < initcmd.userNum; j++) // find the index of the children
            {
                if (userid[j] == waitPid) {
                    //printf("Parent, pid %d :No.%d: User %s ,userpid %d completed execution \n", getpid(), j + 1, initcmd.user[j], waitPid);
                }
            }
        }
        printf("-> Bye! \n");
        exit(0);
    }
}
