#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Service identity verification for pyOpenSSL & cryptography
Summary(pl.UTF-8):	Weryfikacja tożsamości usługi dla modułów pyOpenSSL i cryptography
Name:		python3-service_identity
Version:	24.2.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/service-identity/
Source0:	https://files.pythonhosted.org/packages/source/s/service-identity/service_identity-%{version}.tar.gz
# Source0-md5:	e575db51719742ec39191c896e4c2971
URL:		https://pypi.org/project/service_identity/
BuildRequires:	python3-build
BuildRequires:	python3-hatch-fancy-pypi-readme
BuildRequires:	python3-hatch-vcs
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-attrs >= 19.1.0
BuildRequires:	python3-cryptography
BuildRequires:	python3-pyOpenSSL
BuildRequires:	python3-pyasn1
BuildRequires:	python3-pyasn1_modules
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-myst_parser
BuildRequires:	python3-sphinx-notfound-page
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Use this package if:
- you use pyOpenSSL and don't want to be MITM'ed or
- if you want to verify that a PyCA cryptography certificate is valid
  for a certain hostname or IP address.

%description -l pl.UTF-8
Ten moduł jest przydatny jeśli:
- używamy pyOpenSSL i chcemy uniknąć ataku MITM, lub też
- chcemy zweryfikować, że certyfikat PyCA cryptography jest poprawny
  dla określonej nazwy hosta lub adresu IP.

%package apidocs
Summary:	API documentation for Python service_identity module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona service_identity
Group:		Documentation

%description apidocs
API documentation for Python service_identity module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona service_identity.

%prep
%setup -q -n service_identity-%{version}

%build
%py3_build_pyproject

%if %{with tests} || %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-dev
%endif

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/build-3-dev \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3-dev \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%{py3_sitescriptdir}/service_identity
%{py3_sitescriptdir}/service_identity-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
