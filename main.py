import pymysql
from tabulate import tabulate
from datetime import date,datetime


connection = pymysql.connect(host="localhost", user="root", passwd="1233", database="parking")
cursor = connection.cursor()

def slots():
    try:
        cursor.execute("select * from parking_info")
        date = cursor.fetchall()
        return date
    except Exception as E_dataslots:
        return "slot data error..."

def getDate():
    today = date.today()
    formatted_date = today.strftime('%Y-%m-%d')
    print(today)
    return today

def chargeOfParking(type):
        if type == "car":
            return 150
        elif type == "truck":
            return 250
        elif type == "trolly":
            return 300
        elif type == "other":
            return 350
        elif type == "bus":
            return 200
        elif type == "two wheeler":
            return 100

def totalCharge(tid, typ):
    cursor.execute("select * from transaction_info")
    data = cursor.fetchall()
    print(data)
    rate = chargeOfParking(typ)
    for i in data:
        if i[0] == tid:
            date_format = "%Y-%m-%d"
            en = str(i[2])
            enn = en[0:10]
            a = datetime.strptime(enn, date_format)
            b = datetime.strptime(str(getDate()), date_format)
            delta = b - a
            print(delta)
            z = str(delta)
            y = z[0:len(z) - 12]
            print(int(y))
            if int(y) == 0:
                return rate
            else:
                return rate*int(y)


def slotChk():
    cursor.execute("select * from parking_info")
    data = cursor.fetchall()
    for i,j in data:
        if j == None:
            return i

def vehicleLogin(veh_no,veh_slot,customer_name,customer_no,veh_type):
    cursor.execute("select * from vehicle_info")
    data = cursor.fetchall()
    print(data)
    for i in data:
        if i[2] == veh_slot:
            if i[3] == "Active":
                print("currently slot number \"{}\" is occupied.....".format(veh_slot))
                return "Failed"
    id = cursor.rowcount
    cursor.execute("select * from transaction_info")
    tid = cursor.rowcount
    try:
        query1 = "insert into vehicle_info value({},'{}',{},'{}','{}')".format(id+1,veh_no, veh_slot, "Active",veh_type)
        cursor.execute(query1)
        query2 = "insert into customer_info value('{}',{},{},{})".format(customer_name, customer_no, id+1,tid+1)
        cursor.execute(query2)
        query3 = "update parking_info set slot_status = '{}' where slot_id ={}".format('Parked',veh_slot)
        cursor.execute(query3)
        date = getDate()
        rate = chargeOfParking(veh_type)
        cursor.execute("INSERT INTO transaction_info(transaction_id, Amount, entrydate) VALUES (%s, %s, %s)",(1,rate,getDate()))
        #ADD TRANSACTION DATE
        connection.commit()
        print("Successfully parked your {} at slot \'{}\'  ".format(veh_type, veh_slot))
    except:
        print("something went wrong retry....")
    listf = [("Vehicle_id", "VehicleType", "SlotId", "EntryDate", "RatePerDay")]
    lic = []
    lic.append(id + 1)
    lic.append(veh_type)
    lic.append(veh_slot)
    lic.append(getDate())
    lic.append(chargeOfParking(veh_type))
    listf.append(lic)
    print(tabulate(listf,headers='firstrow',tablefmt='fancy_grid'))


def vehicleLogout():
    vehdata = ()
    cusdata = ()
    cursor.execute("select * from vehicle_info")
    data = cursor.fetchall()
    cursor.execute("select * from customer_info")
    datac = cursor.fetchall()
    veh_id = int(input("Enter vehicle login id: "))
    cursor.execute("select * from parking_info")
    datap = cursor.fetchall()

    try:
        for i in data:
            if i[0] == veh_id:
                vehdata = i
                for j in datac:
                    if i[0] == j[2]:
                        cusdata = j
    except:
        print("Vehicle logout failed.......")
    if vehdata[3] == 'Active':
        query1 = "UPDATE VEHICLE_INFO SET vehicle_status = 'Out' WHERE vehicle_id = {}".format(int(veh_id))
        cursor.execute(query1)
        query2 = "UPDATE PARKING_INFO SET SLOT_STATUS = NULL WHERE slot_id = {}".format(vehdata[2])
        cursor.execute(query2)
        cursor.execute("INSERT INTO transaction_info(exitdate, TotalCharge) VALUES (%s, %s)",(getDate(),totalCharge(cusdata[3]), vehdata[1]))
        exitDate = getDate()
        top = ["Name", "PhoneNumber", "VehicleId", "VehicleNumber", "Type", "EntryDate", "ExitDate", "TotalCharge"]
        details = []
        e = []
        for i in cusdata:
            e.append(i)
            if len(e) == 2:
                print(e)
                break
        e.append(vehdata[0])
        e.append(vehdata[1])
        e.append(vehdata[4])
        e.append(getDate())
        e.append(totalCharge(cusdata[3]), vehdata[1])

        details.append(e)

        print(tabulate(details, headers=top, tablefmt='fancy_grid'))
        connection.commit()
    else:
        print("Vehicle has been already logged out")

def show_customer_details():
    table = []
    col = []
    print("____Customer Details____")
    cursor.execute("select * from customer_info")
    data = [item for item in cursor.fetchall()]
    for column in cursor.description:
        col.append(column[0])
    table.append(col)
    for i in data:
        table.append(i)
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

    connection.commit()

def show_transaction_details():
    table = []
    col = []
    print("____Transaction Details____")
    cursor.execute("select * from transaction_info")
    data = cursor.fetchall()
    for i in cursor.description:
        col.append(i[0])

    print(tabulate(data,headers= col,tablefmt='fancy_grid'))
    connection.commit()

def search():
    print("____Search Parking Menu____")
    print("1.parking slot")
    print("2.customer info")
    print("3.vehicle detail")
    print("0.Leave search")
    cho = int(input("Enter choice to search records: "))
    if cho == 1:
        val = int(input("Enter the parking slot id: "))
        cursor.execute("select * from parking_info")
        data = cursor.fetchall()
        for i in data:
            if val == i[0]:
                if i[1] != None:
                    print("Slot \"{}\" is occupied".format(i[0]))
                else:
                    print("Slot {} is Free now".format(i[0]))
        connection.commit()
    elif cho == 2:
        val = input("Enter the customer name: ").upper()
        cursor.execute("select * from customer_info")
        data = cursor.fetchall()
        li = cursor.description
        l = []
        li = [i[0] for i in li]
        l.append(li)
        for i in data:
            if val in i[0]:
                l.append(i)
        if len(l)>1:
            print(tabulate(l, tablefmt="fancy_grid"),"\n")
        else:
            print("No Data available...\n")
    elif cho == 3:
        val = input("Enter the vehicle number: ").upper()
        cursor.execute("select * from vehicle_info")
        data = cursor.fetchall()
        li = cursor.description
        l = []
        li = [i[0] for i in li]
        l.append(li)
        for i in data:
            if val in i[1]:
                l.append(i)
        if len(l) > 1:
            print(tabulate(l, tablefmt="fancy_grid"), "\n")
        else:
            print("No Data available...\n")
    elif cho == 0:
        return "exit"
    else:
        print("Entered option is not valid..")





while True:
    dataST = slots()
    r = []
    c = []
    tab = []
    distab = []
    print("_____Vehicle Parking Management System____")
    for i in dataST:
        r.append(i)
        if i[1] == None or i[1] == '':
            c.append("Free")
        else:
            c.append(i[1])
        if i[0]%5 == 0:
            tab.append(r)
            distab.append(c)
            r = []
            c = []
    print(tabulate(distab, tablefmt="fancy_grid"))
    print()
    print("____________________________________________")
    print("1.Vehicle login")
    print("2.Vehicle logout")
    print("3.Customer Details")
    print("4.Search Details")
    print("5.Transaction Details")
    print("0.exit")
    opt = int(input("Enter your choice: "))

    if opt == 1:
        Validatae = False
        customer_name = input("Enter customer Name: ").upper()
        customer_no = int(input("Enter customer's phone number:  "))
        if len(str(customer_no)) <= 10:
            veh_no = input("Enter Vehicle number: ").upper()
            if len(veh_no) <= 10:
                veh_type = input("1.car\n2.bus\n3.truck\n4.two wheeler\n5.trolly\n6.other\nEnter type of vehicle:").lower()
                if veh_type in ("car", "truck", "bus", "two wheeler", "trolly", "other"):
                    veh_slot = slotChk()
                    Validatae = True
                else:
                    print("Vehicle type is not proper")
            else:
                print("Vehicle number is not valid")
        else:
            print("Phone number is not valid")
        if Validatae == True:
            vehicleLogin(veh_no, veh_slot, customer_name, customer_no, veh_type)
            pa = input("Press Enter to continue.....")
        else:
            print("retry.....")

    elif opt == 2:
        vehicleLogout()
        pas = input("press Enter to exit...... ")
    elif opt == 3:
        show_customer_details()
        pas = input("press Enter to exit...... ")
    elif opt == 4:
        search()
        pa = input("Press Enter to continue.....")
    elif opt == 5:
        show_transaction_details()
        pas = input("press Enter to exit...... ")
    elif opt == 0:
        break

