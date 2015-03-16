Anshul Jain (AJ) and Marc Lindsay

One thing I realized we need to do - 

	-we'll definitely need a host process running netbin host as a server socket managing connections and the file list, otherwise it's not possible to have a background process autostart.
	-we need a way for new clients to query the network and find the computer running the host.
	-we need to have connections running in the background.
	-we do however need a way for clients to maintain and store file segments
		- architecture ideas: 
			- Host process begins, calls netbin_host
			- Client connects, runs netbin_client
				- lets host know that it exists and is running. if it terminates, then the host



Transferring host reponsibilities

Receiving Host responsibilities

Having host operate as client.


TODO:
	- TRANSFER HOST RESPONSIBILITIES
	- Multithread for large files.