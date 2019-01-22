     paCleanUP
    
    
        Discription: 
            Palo alto firewalls api does not expose a way to delete software from devices.
            downloaded or uploaded images from the device. 
           
            Make a file with one firewall address
            per line set the defaults in the defauts section below.
    
    
        Requires:
            getpass
            netmiko
            requests
            json
            xmltodict
                
                to install try: pip install netmiko xmltodict requests 
    
    
    
        Author:
            Devin Callaway dcallaway@compunet.biz
    
        Tested:
            Tested on macos 12.12.6
            osx system python: 2.7.10
            pa220
    
        Example usage:
            Set default filename username and global timeout in default section below
                $ python deleteUnusedSoftware.py
                Password: 
    
    
       Cautions:
            Diffrent firewalls my require an adjustment to delay factor on any given command
            PA220 
            4 for connection 
            10 for system info
            15 for software info


        Legal:
           THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
            WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
            MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
            ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
            WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
            ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
            OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
       Todo:
          * change the loop to a fuction so not useing continue:
            * test on multiple plaforms
            * change it up to take a csv with diffrent usernames and passwords per firewall.
       """
