// Hong Kong
// Update 25/10/2000 - Use local socks server instead of apsocks.yamato
// Update 23/04/2004 : CR#386553 - KP
//     Change proxy to point to the CISCO Content Engine hkce01 instead of
//     the local proxy as per the BlueIce project.
// Update 26/04/2004 : PR#18921383 - KP
//	Above has been backed out due to a problem with gcgmpacf.hk.ibm.com
// Update 04/05/2004 : CR#417495 - KP
//      Change proxy to point to the CISCO CE as PR#18921383 has been resolved
// Update 14/05/2004 : CR#386554 - KP
//      Use PIX (Direct connection) as opposed to local socks
// Update 07/12/2004 : PR#21883213 - KP
//      Forced nbaxa006.ng.boulder.ibm.com to go DIRECT
// Update 09/12/2004 : PR#22006905 - KP
//      Force ISSI traffic to go DIRECT as per other AP implementations
//alert("DEBUG VERSION\nAutomatic Netscape PROXY configuration by Paul Gunther 1996,1998,1999 \nWARNING Your browser will be difficult to use in debug mode!");
function FindProxyForURL(url, host)
{
// url refers to host on internal network, inside firewall
if (isPlainHostName(host))
{
//alert("DEBUG: ("+url+") Is internal, not cached, local");
return "DIRECT"; // local hosts without domain
}

i = dnsResolve(host);
if ( i == null ) {
        //alert("DNS failed to resolve"+host);
        return "DIRECT";
}        
if ( isInNet (i, "127.0.0.0", "255.0.0.0") ) {
        //alert("local");
        return "DIRECT";
}      
if (isInNet(i, "127.0.0.1", "255.255.255.255")
|| isInNet(i, "9.0.0.0", "255.0.0.0")
|| isInNet(i, "32.71.0.0", "255.255.255.128")
|| isInNet(i, "32.71.114.0", "255.255.255.0")
|| isInNet(i, "32.71.126.32", "255.255.255.224")
|| isInNet(i, "32.71.126.64", "255.255.255.224")
|| isInNet(i, "32.71.126.96", "255.255.255.224")
|| isInNet(i, "32.71.193.128", "255.255.255.128")
|| isInNet(i, "32.71.196.64", "255.255.255.224")
|| isInNet(i, "32.71.234.128", "255.255.255.192")
|| isInNet(i, "32.71.247.192", "255.255.255.192")
|| isInNet(i, "32.72.67.0", "255.255.255.0")
|| isInNet(i, "32.72.234.128", "255.255.255.192")
|| isInNet(i, "32.72.234.192", "255.255.255.240")
|| isInNet(i, "32.72.248.8", "255.255.255.248")
|| isInNet(i, "32.73.0.0", "255.255.248.0")
|| isInNet(i, "32.73.88.0", "255.255.255.0")
|| isInNet(i, "32.73.203.0", "255.255.255.224")
|| isInNet(i, "32.73.204.0", "255.255.255.248")
|| isInNet(i, "32.73.204.6", "255.255.255.255")
|| isInNet(i, "32.73.231.64", "255.255.255.240")
|| isInNet(i, "32.73.235.64", "255.255.255.192")
|| isInNet(i, "32.76.252.128", "255.255.255.224")
|| isInNet(i, "32.76.252.160", "255.255.255.224")
|| isInNet(i, "32.77.2.0", "255.255.255.0")
|| isInNet(i, "32.81.250.64", "255.255.255.224")
|| isInNet(i, "32.81.250.96", "255.255.255.224")
|| isInNet(i, "32.95.128.0", "255.255.254.0")
|| isInNet(i, "32.95.129.0", "255.255.255.240")
|| isInNet(i, "32.95.131.0", "255.255.255.248")
|| isInNet(i, "32.95.132.0", "255.255.255.0")
|| isInNet(i, "32.95.132.0", "255.255.254.0")
|| isInNet(i, "32.95.133.0", "255.255.255.0")
|| isInNet(i, "32.95.225.64", "255.255.255.255")
|| isInNet(i, "32.96.114.0", "255.255.255.0")
|| isInNet(i, "32.96.115.0", "255.255.255.0")
|| isInNet(i, "32.96.116.0", "255.255.255.0")
|| isInNet(i, "32.224.0.0", "255.240.0.0")
|| isInNet(i, "129.33.0.0", "255.255.0.0")
|| isInNet(i, "129.35.0.0", "255.255.0.0")
|| isInNet(i, "129.35.110.0", "255.255.255.0")
|| isInNet(i, "129.36.0.0", "255.255.0.0")
|| isInNet(i, "129.39.126.14", "255.255.255.224")
|| isInNet(i, "129.39.126.15", "255.255.255.224")
|| isInNet(i, "129.39.230.0", "255.255.255.0")
|| isInNet(i, "129.40.0.0", "255.255.0.0")
|| isInNet(i, "129.41.176.0", "255.255.240.0")
|| isInNet(i, "129.41.192.0", "255.255.240.0")
|| isInNet(i, "129.41.208.0", "255.255.240.0")
|| isInNet(i, "129.41.224.0", "255.255.240.0")
|| isInNet(i, "134.56.73.0", "255.255.255.0")
|| isInNet(i, "134.149.0.0", "255.255.0.0")
|| isInNet(i, "138.70.8.0", "255.255.255.0")
|| isInNet(i, "138.95.10.103", "255.255.255.255")
|| isInNet(i, "141.94.0.0", "255.255.0.0")
|| isInNet(i, "141.95.0.0", "255.255.0.0")
|| isInNet(i, "146.84.0.0", "255.255.0.0")
|| isInNet(i, "146.84.3.11", "255.255.255.255")
|| isInNet(i, "147.204.60.0", "255.255.255.0")
|| isInNet(i, "149.174.5.8", "255.255.255.252")
|| isInNet(i, "149.174.220.0", "255.255.255.0")
|| isInNet(i, "150.24.0.0", "255.255.0.0")
|| isInNet(i, "151.104.0.0", "255.255.0.0")
|| isInNet(i, "155.51.0.0", "255.255.0.0")
|| isInNet(i, "158.98.0.0", "255.255.0.0")
|| isInNet(i, "160.100.0.0", "255.255.0.0")
|| isInNet(i, "164.120.0.0", "255.255.0.0")
|| isInNet(i, "165.172.0.0", "255.255.0.0")
|| isInNet(i, "167.210.0.0", "255.255.0.0")
|| isInNet(i, "172.16.1.18", "255.255.255.255")
|| isInNet(i, "172.20.0.0", "255.255.0.0")
|| isInNet(i, "192.1.1.0", "255.255.255.0")
|| isInNet(i, "192.6.37.0", "255.255.255.0")
|| isInNet(i, "192.6.38.0", "255.255.255.0")
|| isInNet(i, "192.9.200.0", "255.255.255.0")
|| isInNet(i, "192.80.11.0", "255.255.255.0")
|| isInNet(i, "192.94.222.0", "255.255.255.0")
|| isInNet(i, "192.108.1.0", "255.255.255.0")
|| isInNet(i, "192.109.81.0", "255.255.255.0")
|| isInNet(i, "192.150.51.0", "255.255.255.0")
|| isInNet(i, "192.150.52.0", "255.255.255.0")
|| isInNet(i, "192.150.53.0", "255.255.255.0")
|| isInNet(i, "192.150.54.0", "255.255.255.0")
|| isInNet(i, "192.150.55.0", "255.255.255.0")
|| isInNet(i, "192.168.1.0", "255.255.255.0")
|| isInNet(i, "192.204.12.0", "255.255.255.0")
|| isInNet(i, "192.204.13.0", "255.255.255.0")
|| isInNet(i, "192.204.14.0", "255.255.255.0")
|| isInNet(i, "192.204.15.0", "255.255.255.0")
|| isInNet(i, "192.216.76.0", "255.255.255.0")
|| isInNet(i, "192.216.77.0", "255.255.255.0")
|| isInNet(i, "192.216.78.0", "255.255.255.0")
|| isInNet(i, "192.216.79.0", "255.255.255.0")
|| isInNet(i, "192.231.9.32", "255.255.255.224")
|| isInNet(i, "192.231.9.64", "255.255.255.224")
|| isInNet(i, "192.231.9.96", "255.255.255.224")
|| isInNet(i, "192.231.9.160", "255.255.255.224")
|| isInNet(i, "192.233.137.0", "255.255.255.0")
|| isInNet(i, "192.233.138.0", "255.255.255.0")
|| isInNet(i, "193.10.1.0", "255.255.255.0")
|| isInNet(i, "193.42.232.0", "255.255.255.0")
|| isInNet(i, "193.64.34.0", "255.255.255.0")
|| isInNet(i, "193.66.138.0", "255.255.255.0")
|| isInNet(i, "193.66.158.0", "255.255.255.0")
|| isInNet(i, "193.78.128.0", "255.255.255.0")
|| isInNet(i, "193.78.129.0", "255.255.255.0")
|| isInNet(i, "193.78.131.0", "255.255.255.0")
|| isInNet(i, "193.106.59.20", "255.255.255.252")
|| isInNet(i, "193.135.16.0", "255.255.255.0")
|| isInNet(i, "194.10.5.0", "255.255.255.0")
|| isInNet(i, "194.10.163.0", "255.255.255.0")
|| isInNet(i, "194.10.166.0", "255.255.255.0")
|| isInNet(i, "194.10.230.0", "255.255.255.0")
|| isInNet(i, "194.32.222.0", "255.255.255.0")
|| isInNet(i, "194.32.222.192", "255.255.255.192")
|| isInNet(i, "194.32.223.0", "255.255.255.0")
|| isInNet(i, "194.32.223.192", "255.255.255.192")
|| isInNet(i, "194.39.240.0", "255.255.255.0")
|| isInNet(i, "194.48.84.0", "255.255.255.0")
|| isInNet(i, "194.147.105.20", "255.255.255.255")
|| isInNet(i, "194.194.32.0", "255.255.255.0")
|| isInNet(i, "194.194.201.0", "255.255.255.0")
|| isInNet(i, "194.194.210.0", "255.255.255.0")
|| isInNet(i, "194.196.110.1", "255.255.255.255")
|| isInNet(i, "194.253.16.0", "255.255.255.0")
|| isInNet(i, "194.253.111.0", "255.255.255.0")
|| isInNet(i, "195.51.214.128", "255.255.255.224")
|| isInNet(i, "196.15.123.80", "255.255.255.240")
|| isInNet(i, "198.49.195.0", "255.255.255.0")
|| isInNet(i, "198.114.0.0", "255.255.192.0")
|| isInNet(i, "198.114.14.0", "255.255.255.0")
|| isInNet(i, "198.114.31.0", "255.255.255.0")
|| isInNet(i, "198.114.32.0", "255.255.255.0")
|| isInNet(i, "198.114.33.0", "255.255.255.0")
|| isInNet(i, "198.114.34.0", "255.255.255.0")
|| isInNet(i, "198.114.35.0", "255.255.255.0")
|| isInNet(i, "198.114.36.0", "255.255.255.0")
|| isInNet(i, "198.114.37.0", "255.255.255.0")
|| isInNet(i, "198.114.38.0", "255.255.255.0")
|| isInNet(i, "198.114.62.0", "255.255.255.0")
|| isInNet(i, "198.114.64.0", "255.255.255.0")
|| isInNet(i, "198.114.65.0", "255.255.255.0")
|| isInNet(i, "198.114.69.0", "255.255.255.0")
|| isInNet(i, "198.114.71.0", "255.255.255.0")
|| isInNet(i, "198.114.72.0", "255.255.255.0")
|| isInNet(i, "198.114.79.0", "255.255.255.0")
|| isInNet(i, "198.114.80.0", "255.255.240.0")
|| isInNet(i, "198.114.95.0", "255.255.255.0")
|| isInNet(i, "198.114.96.0", "255.255.224.0")
|| isInNet(i, "198.114.101.0", "255.255.255.0")
|| isInNet(i, "198.151.127.0", "255.255.255.0")
|| isInNet(i, "198.151.241.0", "255.255.255.0")
|| isInNet(i, "198.182.235.0", "255.255.255.0")
|| isInNet(i, "198.187.134.0", "255.255.255.0")
|| isInNet(i, "199.4.213.44", "255.255.255.252")
|| isInNet(i, "199.4.213.68", "255.255.255.252")
|| isInNet(i, "199.4.213.72", "255.255.255.252")
|| isInNet(i, "199.4.213.76", "255.255.255.252")
|| isInNet(i, "199.4.213.88", "255.255.255.252")
|| isInNet(i, "199.4.213.92", "255.255.255.252")
|| isInNet(i, "199.4.213.108", "255.255.255.252")
|| isInNet(i, "199.4.213.112", "255.255.255.252")
|| isInNet(i, "199.4.213.120", "255.255.255.252")
|| isInNet(i, "199.4.213.124", "255.255.255.252")
|| isInNet(i, "199.201.254.0", "255.255.255.0")
|| isInNet(i, "199.242.142.0", "255.255.255.0")
|| isInNet(i, "199.245.154.0", "255.255.255.0")
|| isInNet(i, "204.69.141.0", "255.255.255.0")
|| isInNet(i, "204.146.91.32", "255.255.255.224")
|| isInNet(i, "204.146.91.64", "255.255.255.224")
|| isInNet(i, "204.146.91.96", "255.255.255.224")
|| isInNet(i, "204.146.91.128", "255.255.255.224")
|| isInNet(i, "204.146.91.160", "255.255.255.240")
|| isInNet(i, "204.146.91.192", "255.255.255.224")
|| isInNet(i, "204.146.104.0", "255.255.255.0")
|| isInNet(i, "204.146.107.0", "255.255.255.0")
|| isInNet(i, "204.146.153.224", "255.255.255.240")
|| isInNet(i, "204.146.240.0", "255.255.255.0")
|| isInNet(i, "204.146.241.0", "255.255.255.0")
|| isInNet(i, "204.146.242.0", "255.255.255.0")
|| isInNet(i, "204.146.243.0", "255.255.255.0")
|| isInNet(i, "204.146.244.0", "255.255.255.0")
|| isInNet(i, "204.146.245.0", "255.255.255.0")
|| isInNet(i, "204.146.246.0", "255.255.255.0")
|| isInNet(i, "204.146.247.0", "255.255.255.0")
|| isInNet(i, "204.146.248.0", "255.255.255.0")
|| isInNet(i, "204.146.249.0", "255.255.255.0")
|| isInNet(i, "204.146.250.0", "255.255.255.0")
|| isInNet(i, "204.146.251.0", "255.255.255.0")
|| isInNet(i, "204.146.252.0", "255.255.255.0")
|| isInNet(i, "204.146.253.0", "255.255.255.0")
|| isInNet(i, "204.146.254.0", "255.255.255.0")
|| isInNet(i, "204.146.255.0", "255.255.255.0")
|| isInNet(i, "204.148.15.0", "255.255.255.0")
|| isInNet(i, "204.160.216.0", "255.255.255.0")
|| isInNet(i, "204.160.217.0", "255.255.255.0")
|| isInNet(i, "205.226.112.0", "255.255.255.0")
|| isInNet(i, "205.226.113.0", "255.255.255.0")
|| isInNet(i, "205.226.114.0", "255.255.255.0")
|| isInNet(i, "205.226.115.0", "255.255.255.0")
|| isInNet(i, "205.226.116.0", "255.255.255.0")
|| isInNet(i, "205.226.117.0", "255.255.255.0")
|| isInNet(i, "205.226.118.0", "255.255.255.0")
|| isInNet(i, "205.226.119.0", "255.255.255.0")
|| isInNet(i, "206.183.53.0", "255.255.255.0")
|| isInNet(i, "206.199.129.176", "255.255.255.240")
|| isInNet(i, "206.199.188.0", "255.255.255.0")
|| isInNet(i, "206.199.192.0", "255.255.255.192")
|| isInNet(i, "206.199.192.64", "255.255.255.240")
|| isInNet(i, "206.199.192.112", "255.255.255.240")
|| isInNet(i, "206.199.252.32", "255.255.255.240")
|| isInNet(i, "206.199.252.64", "255.255.255.224")
|| isInNet(i, "207.146.170.0", "255.255.255.0")) 
{ // internal

// this will go , it is here now to force autoproxy hits
if ( url.substring(0,27) == "http://autoproxy.au.ibm.com" ||
     url.substring(0,21) == "http://w3.gcg.ibm.com" ) {
	// alert("DEBUG: ("+url+") is special no-cache");
	return "DIRECT";
} // if

// proxy caches don't seem to handle non-ibm sites
//if  ( ! dnsDomainIs(host, "ibm.com") )  {
	//alert("DEBUG: ("+url+") is internal, not ibm");
//	return "DIRECT";
//}

// force hits for sbygad03.sby.ibm.com to go direct
if ( url.substring(5,27) == "//sbygad03.sby.ibm.com" ) {
        //alert("DEBUG: ("+url+") is special no-cache");
        return "DIRECT";
} // if

// force hits for hn.hk.ibm.com to go direct
if ( url.substring(5,20) == "//hn.hk.ibm.com" ) {
        //alert("DEBUG: ("+url+") is special no-cache");
        return "DIRECT";
} // if

// force hits for mn.hk.ibm.com to go direct
if ( url.substring(5,20) == "//mn.hk.ibm.com" ) {
        //alert("DEBUG: ("+url+") is special no-cache");
        return "DIRECT";
} // if


// force hits for 9.186.0.152 to go direct
if ( url.substring(5,23) == "//w3-1.gcg.ibm.com" ) {
        //alert("DEBUG: ("+url+") is special no-cache");
        return "DIRECT";
} // if

// force hits for 9.186.0.152 to go direct
if ( url.substring(5,21) == "//w3.gcg.ibm.com" ) {
        //alert("DEBUG: ("+url+") is special no-cache");
        return "DIRECT";
} // if


// force hits for 9.186.0.153 to go direct
if ( url.substring(5,21) == "//w4.gcg.ibm.com" ) {
        //alert("DEBUG: ("+url+") is special no-cache");
        return "DIRECT";
} // if

// force hits for  to go direct
if ( url.substring(5,15) == "//gcgmpacf" ) {
        //alert("DEBUG: ("+url+") is special no-cache");
        return "PROXY hkproxy.hk.ibm.com; PROXY hkce01.hk.ibm.com; DIRECT";
} // if

// force hits for nbaxa006.ng.boulder.ibm.com to go direct
if ( url.substring(5,34) == "//nbaxa006.ng.boulder.ibm.com" ) {
        return "DIRECT";
} // if

if (url.substring(0,34) == "ftp://ncosdcf.au.ibm.com/NAV/LUFTP") {
   return "DIRECT";
}

// Force ISSI traffic to go DIRECT as per PR#21547722
if ( url.substring(5,46) == "//w3-1.ibm.com/download/standardsoftware/" ) {
        return "DIRECT";
} // if

if ( url.substring(0,5) == "http:" ||
     url.substring(0,4) == "ftp:" ||
   url.substring(0,6) == "https:" ||  // not cached, transparent
     url.substring(0,7) == "gopher:" )  // can be cached
{ // true
	//alert("DEBUG: ("+url+") is internal, cached");
       return "PROXY hkce01.hk.ibm.com:80; PROXY 9.181.193.210:80; DIRECT";
} else { // cannot be cached
	//alert("DEBUG: ("+url+") is internal, not cached");
	return "DIRECT"; 
} // else
} // internal

// external
if ( (url.substring(0,5) == "http:" ||
     url.substring(0,4) == "ftp:" ||
   url.substring(0,6) == "https:" ||  // not cached, transparent
     url.substring(0,7) == "gopher:") )  // can be cached
{ // true
	//alert("DEBUG: ("+url+") is external, cached");
       return "PROXY hkce01.hk.ibm.com:80; PROXY 9.181.193.210:80; DIRECT";
} else { // cannot be cached - https, nntp, snews, wais, telnet , ssh ...
	//alert("DEBUG: ("+url+") is external, not cached");
	return "DIRECT";
}  // else
} // Findproxy
