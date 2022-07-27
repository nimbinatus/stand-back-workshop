# Lab 00.02: Getting the Pulumi CLI

Next, you'll need the Pulumi CLI. Depending on what system you're running, you'll need different tools. The most recent version of this guide can be found on [Pulumi's CLI install](https://www.pulumi.com/docs/get-started/install/#installing-pulumi?utm_source=laura&utm_medium=developer-advocate&utm_campaign=kcdc2022) page, but here it is in case you need it.

- [MacOS](#macos)
- [Windows](#windows)
- [Linux](#linux)

## MacOS

There are four ways to install the Pulumi CLI on MacOS.
- [Homebrew](#homebrew)
- [MacPorts](#macports)
- [Installation script](#macos-installation-script)
- [Manual installation](#macos-manual-installation)

### Homebrew
The best way and the way I'd recommend is via Homebrew and the official tap:

```bash
$ brew install pulumi/tap/pulumi
```

### MacPorts

If you don't want to use Homebrew, you can use Macports:

```bash
$ sudo port install pulumi
```

### MacOS Installation Script

If you don't use Homebrew or MacPorts, you can use the install script via CURL:

```bash
$ curl -fsSL https://get.pulumi.com | sh
```

### MacOS Manual Installation

If none of those work for you, you can install manually.

1. Download the latest version from the [Available Versions](https://www.pulumi.com/docs/get-started/install/versions/?utm_source=laura&utm_medium=developer-advocate&utm_campaign=kcdc2022) page. For prior versions and release notes, reference the [Available Versions](https://www.pulumi.com/docs/get-started/install/versions/?utm_source=laura&utm_medium=developer-advocate&utm_campaign=kcdc2022) page.
1. Extract the tarball and move the binaries in the `pulumi` directory to a directory included in your system's `$PATH`.

## Windows

There are five ways to install the Pulumi CLI on Windows.

- [Chocolatey](#chocolatey)
- [Winget](#winget)
- [Standalone installer](#standalone-installer)
- [Installation script](#windows-installation-script)
- [Manual installation](#windows-installation-script)

### Chocolatey

You can install Pulumi using elevated permissions through the [Chocolatey package manager](https://chocolatey.org/):

```
> choco install pulumi
```

This command will install the Pulumi CLI to the usual place (often `$($env:ChocolateyInstall)\lib\pulumi`) and generate the shims (usually `$($env:ChocolateyInstall)\bin`) to add the Pulumi CLI your path.

### Winget

Install Pulumi using the [winget-cli](https://github.com/microsoft/winget-cli/) package manager. This tool is built-in on Windows 11 and later.

```
> winget install pulumi
```

### Standalone Installer

You can download the [latest Pulumi CLI Installer for Windows x64](https://github.com/pulumi/pulumi-winget/releases) and run it like any other installer. It will automatically add the Pulumi CLI to the path and make it available machine-wide.

### Windows Installation Script

Open a new command prompt window (**WIN+R**: `cmd.exe`):

Run the installation script:

```
> @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://get.pulumi.com/install.ps1'))" && SET "PATH=%PATH%;%USERPROFILE%\.pulumi\bin"
```

This command will install the `pulumi.exe` CLI to `%USERPROFILE%\.pulumi\bin` and add it to your path.

### Windows Manual Installation

Alternatively, you can install Pulumi manually using binaries built for Windows x64.

1. Download the latest version from the [Available Versions](https://www.pulumi.com/docs/get-started/install/versions/?utm_source=laura&utm_medium=developer-advocate&utm_campaign=kcdc2022) page. For prior versions and release notes, reference the [Available Versions](https://www.pulumi.com/docs/get-started/install/versions/?utm_source=laura&utm_medium=developer-advocate&utm_campaign=kcdc2022) page.
1. Unzip the file and extract the contents to a folder, such as `C:\pulumi`.
1. Add `C:\pulumi\bin` to your path via **System Properties** > **Advanced** > **Environment Variables** > **User Variables** > **Path** > **Edit**.

## Linux

There are two ways to install the Pulumi CLI on a Linux box.

- [Install script](#linux-installation-script)
- [Manual install](#linux-manual-installation)

### Linux Installation Script

To install, run this installation script:

```
curl -fsSL https://get.pulumi.com | sh
```

This command will install the Pulumi CLI to `~/.pulumi/bin` and add it to your path. When it can't automatically add `pulumi` to your path, you will be prompted to add it manually. See [How to permanently set $PATH on Unix](https://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux-unix) for guidance.

### Linux Manual Installation

Alternatively, you can install the Pulumi CLI manually. There is a prebuilt binary for Linux.

1. Download the latest version from the [Available Versions](https://www.pulumi.com/docs/get-started/install/versions/?utm_source=laura&utm_medium=developer-advocate&utm_campaign=kcdc2022) page. For prior versions and release notes, reference the [Available Versions](https://www.pulumi.com/docs/get-started/install/versions/?utm_source=laura&utm_medium=developer-advocate&utm_campaign=kcdc2022) page.
1. Extract the tarball and move the binaries in the `pulumi` directory to a directory included in your system's `$PATH`.
