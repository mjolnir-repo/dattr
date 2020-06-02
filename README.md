> # DATTR: Attribute interpretation of Dictionary Keys
This package was developed as support package to `mjonir` project. In `mjolnir` project, there are certain scope to read configuration json and traverse through then recursively. So I felt the need for a solution that will let us chain the dictionary keys with dot notation for ease-of-use. Hence I built one. I know there are already some libraries available which do similar stuff. But the purpose of this package was to support custom features like reading-writing to-fro json files, read strings and compile as dictionary directly etc.

> ## Features
As already mentioned, main feature of the package is to support attribute style key handling of python dictionaries. It will also continue to support interpolation. Following are some example:
### 1. Convert a dictionary to dattr:
User needs to create an object of the `Dictattr` class to get the features, e.g.

    => import dattr
    => d = {'id' : 1, 'name' : {'first' : 'saumalya', 'last': 'sarkar'}, 'student' : True}
    => new_d = dattr.DictAttr(d)
    => print(new_d.id)
    1
    => print(new_d.name.first)
    2

Looks fun, isn't it.
### 2. Create dattr directly from json data:
The same object can be created by directly reading JSON data, e.g.

    => import dattr
    => dattr_obj = dattr.DictAttr.from_string('{"id" : 1, "name" : {"first" : "saumalya", "last": "sarkar"}, "student" : true}')
    => dattr_obj.student == Ture
    True

__*N.B.*__ Use class method `from_json_file` to create object directly from JSON files.

### 3. Access values using interpolation or dot notation:
The choice is mostly user's (check caveat section). User can choose between using interpolation or dot notation while accessing values using keys or assigning values to certain key. e.g.

    => import dattr
    => dattr_obj = dattr.DictAttr({"id" : 1, "name" : {"first" : "saumalya", "last": "sarkar"}, "student" : true})
    => print(dattr_obj.id)
    1
    => print(dattr_obj.name.first)
    saumalya
    ...
    => print(dattr_obj['id'])
    1
    => print(dattr_obj['name']['first'])
    saumalya
### 4. Assigning values using interpolation or dot notation:
The same logic holds while assigning values to, e.g.

    => import dattr
    => dattr_obj = dattr.DictAttr({"id" : 1, "name" : {"first" : "saumalya", "last": "sarkar"}, "student" : true})
    => dattr_obj.id = 2
    => print(dattr_obj.id)
    2
    => dattr_obj.name.middle = "atanu"
    => print(dattr_obj.name.middle)
    atanu
    ...
    => dattr_obj['id'] = 3
    => print(dattr_obj['id'])
    3
    => dattr_obj['name']['middle'] = "na"
    => print(dattr_obj['name']['middle'])
    na
### 5. All existing dictionary APIs will work:
All dictionary methods and attributes will be available, e.g.:

    => import dattr
    => dattr_obj = dattr.DictAttr({"id" : 1, "name" : {"first" : "saumalya", "last": "sarkar"}, "student" : true})
    => dattr_obj.keys()
    dict_keys(['id', 'name', 'student'])
That will be all. Rest is pretty similar to existing dictionary objects.
> ## Caveats
### 1. Key matches object attribute issue:
If any key matches any object attributes, e.g. if data has a key `keys`, then it is mandatory to use interpolation style, or else exceptions may appear.
### 2. Built-in method support:
Some python buil-in methods that operate on dictionaries, may not work on this object. As I did not have such requirements in `mjolnir` project, I skipped that part. Feel free to form the repository and code along.
### 3. Type integrity not maintained:
Python built-in function will always return `<class 'dattr.main.DictAttr'>` as output of `type(dattr_obj)`, irrespective of the actual type of the data.

Alright then, If you can live with the Caveats, feel free to use the package. PYPI details will be added once it is converted. For now cloning is only option. If anyone feels the caveats are a little too much, please notify me. I try to add the required features. Or else anyone is welcome to fork and contribute.

*Thanks, Saumalya Out!*