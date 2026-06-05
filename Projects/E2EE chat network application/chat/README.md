# COMP3334-GP5
3.8
All subdomains *.comp3334.xavier2dc.fr will redirect to 127.0.0.1 
Linux: 

Open a terminal.

sudo nano /etc/hosts

Add the following line at the end of the file:
127.0.0.1 *.comp3334.xavier2dc.fr
Save the changes and exit the text editor. 

Windows:

Open File Explorer.
Navigate to the following directory:
C:\Windows\System32\drivers\etc\
Copy the hosts file to your desktop or any other location.
Open the copied hosts file using a text editor
Add the following line at the end of the file:

127.0.0.1 *.comp3334.xavier2dc.fr

Save the changes to the hosts file.

Copy the modified hosts file back to the original location(C:\Windows\System32\drivers\etc), replacing the existing file. Administrator permissions may be required.


3.10
To install a certificate on a PC

Windows
https://learn.microsoft.com/en-us/skype-sdk/sdn/articles/installing-the-trusted-root-certificate
Linux
https://ubuntu.com/server/docs/security-trust-store

install chatapp.crt only
