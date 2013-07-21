import config
import lib.term
import email.mime.text
import smtplib
import getpass

def send(project,src,dest,snap_dest,smtpserver='localhost',login=None,ssl=False):
    '''Sends out a wentlive email saying that a project has been snapped'''

    lib.term.print_c("Type in a description for a wentlive email.\nAn empty line indicates the end of the description\n",lib.term.BLUE)
    description = lib.term.blockread()

    wentlive = """
Snapper:     {0}
Project:     {1}
Destination: {2}
Branch:      {3}
Commit Hash: {4}
Commit Message: {5}

{6}
 - Snaps

""".format(
    getpass.getuser(),
    project.name,
    snap_dest,
    project.current_branch(),
    project.current_commit(),
    project.current_commit_message(),
    description
)

    wentlive_subject = "WENTLIVE: {0} to {1}".format(project.name,snap_dest)

    if config.testmode:
        print("Wentlive would send email:\n{0}\n{1}\n\nto {2}".format(wentlive_subject,
                                                                      wentlive,
                                                                      dest))
        return

    msg = email.mime.text.MIMEText(wentlive)
    msg['Subject'] = wentlive_subject
    msg['From'] = src

    if type(dest) is list:
        msg['To'] = ", ".join(dest)
    else:
        msg['To'] = dest

    server = None
    if ssl: server = smtplib.SMTP_SSL(smtpserver)
    else:   server = smtplib.SMTP(smtpserver)

    if not login is None:
        [user,password] = login.split(':',1)
        server.login(user,password)

    server.sendmail(src,dest,msg.as_string())
    server.quit()

