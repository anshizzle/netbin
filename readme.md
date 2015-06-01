### About 
Netbin is a command line filesharing utility for Local Area Networks. Devices on the same subnet can upload and download files using the netbin client.



##### Install Netbin:

```
> python setup.py install
```

##### Run Netbin with

```
> netbin
```

#### Commands

Upload files with `> upload filename` or `> ul filename`
Download files from the directory with `> download src dest`  or `> dl src dest` 
List files from the directory with `> list` or `> ls`
Exit the client with `> exit`




### To-Do's

* Transferring host reponsibilities and error handling better.
* Documentation
* Have netbin_files dir be created into root path.
* Have netbin init daemonize, and then other processes plug into the netbin client/host
* Encryption


####
Created by Anshul Jain and Marc Lindsay w/ help from Chris and Richard



