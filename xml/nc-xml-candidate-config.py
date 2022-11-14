#### XML Parsing and Regular Expressions -- difficult, prefer xmltodict
#### DEVASC LAB 3.6.6
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print('Starting  -- XML Parsing')
import xml.etree.ElementTree as ET
import re  # regular expressions
doc =   """
        <?xml version="1.0" encoding="UTF-8"?>
        <rpc message-id="1"
         xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <edit-config>
        <target>
           <candidate/>
        </target>
        <default-operation>merge</default-operation>
        <test-option>set</test-option>
        <config>
           <int8.1
            xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"
            nc:operation="create"
            xmlns="http://netconfcentral.org/ns/test">9</int8.1>
        </config>
        </edit-config>
        </rpc>
    """
#print(doc)
####
print('-----1-----')
#xml_in = ET.parse(doc)
xml_in = ET.parse("netconf-file.xml")
print("Showing XML root data read from external file")
print(xml_in)
root = xml_in.getroot()
print('-----1B-----')
print(root.tag)
print('-----1C-----')
print("XML namespace")
#### Below <.*> => match an entire string
####‼ group() Return the string matched by the RE
ns = re.match('{.*}', root.tag).group(0)
print(ns)
print(type(ns))
#print('-----1D-----')
#print("Traversing root")
#print(dir(root))
#for it in root.iter():
#    print(it)
print('-----2------')
print("Showing XML keys parsed")
nc_data = root.keys()
print(nc_data)
#### Below: {} is a placeholder for Python string formatting
editconf = root.find("{}edit-config".format(ns))
#print(type(editconf))
#print(dir(editconf))
for it in editconf.iter():
    #print(type(it))
    print(it)
print('-----3------')
print("Extracting netconf operations")
defop = editconf.find("{}default-operation".format(ns))
testop = editconf.find("{}test-option".format(ns))
print(defop.text)
print(testop.text)

