import argparse
import json
import subprocess
import regex as re


class Function:
    name: str
    file: str
    start_line: int
    calls: list['Function']
    called_by: list['Function']


    def __init__(self, name: str, file:str, start_line:int):
        self.name = name
        self.file = file
        self.start_line = start_line
        self.calls = []
        self.called_by = []
    

    def add_call(self, call: 'Function') -> None:
        if call not in self.calls:
            self.calls.append(call)
        call.add_called_by(self)


    def add_called_by(self, caller: 'Function') -> None:
        if caller not in self.called_by:
            self.called_by.append(caller)
    

    def __hash__(self) -> int:
        return hash((self.name, self.file, self.start_line))
    

    def __eq__(self, other) -> bool:
        if not isinstance(other, Function):
            return NotImplemented
        return ((self.name, self.file, self.start_line) == (other.name, other.file, other.start_line))
    
    
    def __str__(self) -> str:
        return "File: " + self.file + "\nName: " + self.name + "\nLine: " + str(self.start_line) + "\nCalls: " + str(self.calls) + "\nCalled by: " + str(self.called_by)

    

def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="The string path for the project of analysis")
    return parser.parse_args()


def process_project(project_path:str) -> None:
    p = subprocess.Popen("ctags  --output-format=json --fields=+n -R * > tags.json", shell=True, cwd=project_path)
    p.wait()


def process_json(project_path:str, files:dict[str,list[Function]], functions:list[Function], function_names:dict[str:list[Function]]) -> None:
    lines = []
    with open(project_path + "/tags.json") as data:
        for line in data:
            lines.append(json.loads(line))
    
    for line in lines:
        if line['kind'] == 'function' or line['kind'] == 'method':
            line_number = int(line['line'])
            name = line['name']
            file = line['path']
            new = Function(name, file, line_number)
            if name in function_names:
                print("Duplicate Found: " + name + "\nOriginal: " + str(function_names[name][0]) +"\nNew: " + str(new))
                function_names[name].append(new)
                print("")
            else:
                function_names[name] = [new]
            if file in files:
                files[file].append(new)
            else:
                files[file] = [new]
            functions.append(new)


def organize_files(files:dict[str,list[Function]]) -> None:
    for key in files:
        files[key] = sorted(files[key], key=lambda x: x.start_line)


def find_calls(project_path: str, files:dict[str,list[Function]], function_names:dict[str:list[Function]]) -> None:
    pattern = "(?<=[\s\W]|^)[A-Za-z_]+(?=\()"
    for f in files:
        with open(project_path + "/" + f) as f_read:
            full_text = f_read.readlines()
            for i in range(len(full_text)):
                line = full_text[i]
                matches = re.findall(pattern, line)
                for match in matches:
                    if match in function_names:
                        caller_line = i + 1
                        caller = None
                        for function in files[f]:
                            if function.start_line == caller_line:
                                break
                            elif function.start_line < caller_line:
                                caller = function
                                break
                        if caller is not None:
                            for function in function_names[match]: # Currently calls all duplicates. Can add special cases
                                caller.add_call(function)
                            

def main() -> None:
    args = handle_args()
    process_project(args.path)
    files = {}
    functions = []
    function_names = {}
    process_json(args.path, files, functions, function_names)
    organize_files(files)
    find_calls(args.path, files, function_names)
    

if __name__ == '__main__':
    main()