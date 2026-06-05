Project title: APpointment Organizer (APO) 

Setup:
gcc G25_APO.c -o G25_APO

Run:
./G25_APO YYYYMMDD YYYYMMDD u1 u2 u3 
e.g.  ./G25_APO 20230401 20230430 john mary lucy paul

cmd privateTime:
privateTime uuu YYYYMMDD hhmm n.n 
e.g. privateTime paul 20230401 1800 2.0 

cmd projectMeeting
projectMeeting uuu YYYY-MM-DD hh:mm n.n u1 u2 … 
e.g. projectMeeting john 20230402 1900 2 paul mary 

cmd groupStudy
groupStudy uuu YYYYMMDD hhmm n.n u1 u2 … 
e.g. groupStudy paul 20230403 1800 2.0 john lucy 

cmd gathering
gathering uuu YYYYMMDD hhmm n.n u1 u2 … 
e.g. gathering lucy 20230404 1900 4.0 john paul mary 

cmd printSchd
printSchd sssss / ALL  
e.g. printSchd FCFS 
     [Exported file: Ggg_01_FCFS.txt] 

cmd endProgram
endProgram