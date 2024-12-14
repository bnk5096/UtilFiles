included_extensions = [ ".c", ".cpp", ".h", ".py" ]

with open('/home/axmvse/UtilFiles/ffmpeg_git_ls_tree.txt') as f:
    data = f.readlines()
    for line in data:
        filename = line.strip()
        for ext in included_extensions:
            if filename.endswith(ext):
                print(filename)


