%define real_name MigrationTools

Name:		migrationtools
Version:	45
Release:	%mkrel 2
License:	BSD-like
URL:		http://www.padl.com/OSS/MigrationTools.html
Summary:	Tools for migrating local/NIS account information to LDAP
Group:		System/Configuration/Other
Obsoletes:	openldap-migration <= 2.3.4
Provides:	openldap-migration = %{version}
Provides:	%{real_name} = %{version}-%{release}
Requires:	openldap-clients
Source:		http://www.padl.com/download/%{real_name}-%{version}.tar.bz2
Source3:        migration-tools.txt
Source4:        migrate_automount.pl
Patch40:        MigrationTools-34-instdir.patch
Patch41:        MigrationTools-36-mktemp.patch
Patch42:        MigrationTools-27-simple.patch
Patch43:        MigrationTools-26-suffix.patch
Patch44:        MigrationTools-24-schema.patch
Patch45:        MigrationTools-45-i18n.patch
Patch48:        MigrationTools-45-structural.patch
Patch54: 	MigrationTools-40-preserveldif.patch
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
%patch48 -p2 -b .account
%patch54 -p1 -b .preserve
cp %{SOURCE3} .

%build

perl -pi -e 's,%{_datadir}/openldap/migration,%{_datadir}/%{name},g' *.pl *.sh *.ph
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

