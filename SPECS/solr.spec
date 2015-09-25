# TODO:
# - how to add to the trusted service of the firewall?

%define __os_install_post \ /usr/lib/rpm/brp-compress \ %{!?__debug_package:/usr/lib/rpm/brp-strip %{__strip}} \ /usr/lib/rpm/brp-strip-static-archive %{__strip} \ /usr/lib/rpm/brp-strip-comment-note %{__strip} %{__objdump} \ %{nil}
%define org cn
#%define workdir %{_var}/lib/solr
%define workdir /cn/runtime/solr
%define start_script_path /usr/lib/systemd/system/solr.service

Name:           %{org}-solr
Version:        %{ver}
Release:        %{rel}
Summary:        Apache Search Server
Source:         solr-%{version}.tgz
Source1:        solr.service.in
Source2:        solr.sysconfig.in
Source3:        solr.in.sh.in
URL:            http://lucene.apache.org/solr/
Group:          Development/Tools/Building
License:        Apache License, Version 2.0
BuildRoot:      %{_tmppath}/build-%{name}-%{version}
Requires:       /usr/sbin/groupadd, /usr/sbin/useradd, systemd, java-headless >= 1:1.8.0
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

%__install -D -m0755 "%{SOURCE1}" "%{buildroot}%{start_script_path}"

%__install -D -m0600 "%{SOURCE2}" "%{buildroot}/etc/sysconfig/solr"
%__install -D -m0600 "%{SOURCE3}" "%{buildroot}%{workdir}/bin/solr.in.sh"
%__sed -i 's,@@HOME@@,%{workdir}/server/solr,g' "%{buildroot}/etc/sysconfig/solr"
%__sed -i 's,@@PKG_ROOT@@,%{workdir},g' "%{buildroot}%{start_script_path}"
%__sed -i "s,@@HOSTNAME@@,`hostname`,g" "%{buildroot}/etc/sysconfig/solr"

%pre
/usr/sbin/groupadd -r solr &>/dev/null || :
/usr/sbin/useradd -g solr -s /bin/false -r -c "Solr Search Server" \
        -d "%{workdir}" solr &>/dev/null || :

%post
/usr/bin/systemctl daemon-reload

%preun
if [ "$1" = 0 ] ; then
    # if this is uninstallation as opposed to upgrade, delete the service
    /usr/bin/systemctl stop solr > /dev/null 2>&1
    /usr/bin/systemctl disable solr
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
    /usr/bin/systemctl restart solr > /dev/null 2>&1
fi
exit 0

%clean
%__rm -rf "%{buildroot}"

%files
%defattr(-,solr,solr)
%attr(0755,solr,solr) %{workdir}
%config(noreplace) %{start_script_path}
%config(noreplace) /etc/sysconfig/solr

%changelog
* Wed Sep 11 2013 bwong114@gmail.com
- Added JDBC driver

* Thu Dec 20 2012 bwong114@gmail.com
- First version
