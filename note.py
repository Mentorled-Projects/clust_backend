import smtplib

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("akinrogundep0@gmail.com", "jpko lhpo nvzi nlpl")
server.sendmail(
    "CLUST",
    "akinrogundecodenamemomi@gmail.com",
    "Subject: Test\n\nThis is a test email."
)
server.quit()
