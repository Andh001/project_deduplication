cd Server
d=`pwd`
cd Main_Server
gnome-terminal --geometry=30x15 -e 'python Main.py'

cd ../s1
gnome-terminal --geometry=30x15 -e 'python server_1.py'
cd ../s2
gnome-terminal --geometry=30x15 -e 'python server_2.py'
cd ../s3
gnome-terminal --geometry=30x15 -e 'python server_3.py'
cd ../s4
gnome-terminal --geometry=30x15 -e 'python server_4.py'
cd ../s5
gnome-terminal --geometry=30x15 -e 'python server_5.py'
cd "../../Client"
d=`pwd`

gnome-terminal --geometry=30x15 -e 'python client.py'
