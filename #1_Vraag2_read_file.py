import os

def read_file():
    file_name = str(input("<<Please enter filename (.TXT extension not needed)>>: "))
    filenameraw = file_name + ".txt"
    try:
        with open (filenameraw) as f:
            contents = f.readlines()
            file_size = os.path.getsize(filenameraw)
        with open (filenameraw) as f:
            lines = len(f.readlines())
            print("<<File read successfully!>>")
            view_content = input("Want to know the number of songs it contains(y/n)? ")
            if view_content == 'y':             
                print("Here the song/s in the file:\n")
                for index, song in enumerate(contents,1):
                    print(index,song)               
                print("\n<<Number of songs in file:",lines,"song/s.>>")
                print("<<File size is",file_size,"bytes>>\n")              
            elif view_content == 'n':
                print("\n<<No worries, we'll show you the songs before importing.>>")
            else:
                print("<<Invalid Input! Input must be either YES(y) or NO(n)>>")
    except FileNotFoundError:
        print("<<Sorry we couldn't find " + filenameraw + " may not exist or typo error>>")
read_file()