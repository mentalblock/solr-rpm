# TODO:
# - how to add to the trusted service of the firewall?

%define workdir %{_var}/lib/solr

Name:           nypl-solr
Version:        %{ver}
Release:        %{rel}
Summary:        Apache Search Server
Source:         solr-%{version}.tgz
Source1:        solr.init.in
Source2:        solr.sysconfig.in
Source3:        mysql-connector-java-5.1.26-bin.jar
URL:            http://lucene.apache.org/solr/
Group:          Development/Tools/Building
License:        Apache License, Version 2.0
BuildRoot:      %{_tmppath}/build-%{name}-%{version}
Requires:       /usr/sbin/groupadd /usr/sbin/useradd
BuildArch:      noarch

%description
Solr is a standalone enterprise search server with a REST-like API.

%prep
%setup -q -c

%build

%install
rm -rf "%{buildroot}"
%__install -d "%{buildroot}%{workdir}"
cp -Rp solr-%{version}/* "%{buildroot}%{workdir}"

%__install -d "%{buildroot}/var/log/solr"

%__install -D -m0755 "%{SOURCE1}" "%{buildroot}/etc/init.d/solr"

%__install -D -m0600 "%{SOURCE2}" "%{buildroot}/etc/sysconfig/solr"
%__sed -i 's,@@HOME@@,%{workdir},g' "%{buildroot}/etc/sysconfig/solr"

SOURCE3_FILE=`basename %{SOURCE3}`
%__install -D -m0755 "%{SOURCE3}" "%{buildroot}%{workdir}/contrib/jdbc/lib/${SOURCE3_FILE}"

%pre
/usr/sbin/groupadd -r solr &>/dev/null || :
/usr/sbin/useradd -g solr -s /bin/false -r -c "Solr Search Server" \
        -d "%{workdir}" solr &>/dev/null || :

%post
/sbin/chkconfig --add solr

%preun
if [ "$1" = 0 ] ; then
    # if this is uninstallation as opposed to upgrade, delete the service
    /sbin/service solr stop > /dev/null 2>&1
    /sbin/chkconfig --del solr
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
    /sbin/service solr condrestart > /dev/null 2>&1
fi
exit 0

%clean
%__rm -rf "%{buildroot}"

%files
%defattr(-,root,root)
%attr(0755,solr,solr) %{workdir}
%attr(0755,solr,solr) /var/log/solr
%config(noreplace) /etc/init.d/solr
%config(noreplace) /etc/sysconfig/solr

%changelog
* Wed Sep 11 2013 bwong114@gmail.com
- Added JDBC driver

* Thu Dec 20 2012 bwong114@gmail.com
- First version
