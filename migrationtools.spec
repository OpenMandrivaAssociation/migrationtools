%define real_name MigrationTools
%define name migrationtools
%define version 47
%define release %mkrel 8

Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
URL:		http://www.padl.com/OSS/MigrationTools.html
Summary:	Tools for migrating local/NIS account information to LDAP
Group:		System/Configuration/Other
Provides:	%{real_name} = %{version}-%{release}
Requires:	openldap-clients
Source:		http://www.padl.com/download/%{real_name}-%{version}.tar.bz2
Source3:        migration-tools.txt
Source4:        migrate_automount.pl
Patch40:        MigrationTools-47-instdir.patch
Patch41:        MigrationTools-36-mktemp.patch
Patch42:        MigrationTools-47-simple.patch
Patch43:        MigrationTools-47-suffix.patch
Patch44:        MigrationTools-24-schema.patch
Patch45:        MigrationTools-45-i18n.patch
# http://bugzilla.padl.com/show_bug.cgi?id=236
Patch46:        MigrationTools-47-dc.patch
Buildarch:	noarch
Buildroot:	%{_tmppath}/%{name}-%{version}-root

%description
The MigrationTools are a set of Perl scripts for migrating users, groups,
aliases, hosts, netgroups, networks, protocols, RPCs, and services from 
existing nameservices (flat files, NIS, and NetInfo) to LDAP.

Please note that the migration scripts honour the following environment
variables:

DEFAULT_MAIL_DOMAIN
LDAPADD 	Path the ldapadd executable, for online migration
LDIF2LDBM	Path the ldif2ldbm executable
LDAPHOST	Your LDAP server, for online migration.
LDAP_BASEDN
LDAP_BINDDN	The distinguished name to bind to the LDAP server as, for online
		migration.
LDAP_BINDCRED	The password to bind to the LDAP server with, for online 
		migration.

%prep
%setup -q -n %{real_name}-%{version}
%patch40 -p1 -b .instdir
%patch41 -p1 -b .mktemp
%patch42 -p1 -b .simple
%patch43 -p1 -b .suffix
%patch45 -p2 -b .i18n
%patch46 -p1 -b .dc
cp %{SOURCE3} .

%build

perl -pi -e "s,'migrate_common\.ph','%{_datadir}/%{name}/migrate_common.ph',g" *.pl *.sh *.ph

%install
rm -Rf %{buildroot}

install -d %{buildroot}%{_datadir}/%{name}
install -m 755 {*.pl,*.sh,*.txt,*.ph} %{buildroot}%{_datadir}/%{name}
install -m 755 %{SOURCE4} %{buildroot}%{_datadir}/%{name}
#install -m 644 MigrationTools-%{migtools_ver}/README %{SOURCE3} %{buildroot}%{_datadir}/%{name}

%clean
rm -Rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/%{name}
%doc README migration-tools.txt

