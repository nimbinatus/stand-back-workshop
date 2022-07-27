# Stand Back! (The Workshop) <br/><small>Building a scientific computing lab on public clouds with Python</small>

This workshop is a four-hour workshop for KCDC 2022.

## Goals

- Build a basic scientific computing lab on a public cloud
- Understand how cloud-based infrastructure is put together
- Decipher cloud computing catalogues from different public cloud providers
- (Bonus) Explore the concept of platform engineering

## Equipment, Tools, and Knowledge

You'll need the following equipment:

* A computer running either Linux (any flavor, updated to the most current LTS or higher), MacOS (Sierra 10.12 or later), or Windows (8 or later)
    * Please have a connection outside of a VPN, appropriate debugging skills for your corporate VPN, or have a very good friend in your company's IT department who can help you debug any connection issues on your own.

You'll need the following tools:
* Git 2.x
* Python 3.9+ (prefer 3.10.x)
* An IDE of your choosing.
    * I prefer either PyCharm or VSCode. If you don't know how to do something, raise your hand and ask.
* A free Pulumi SaaS account and token
    * If you don't have an account, go to the signup page.
* The Pulumi CLI
* A free-tier account on GCP and AWS **with admin access**

You'll need the following knowledge:
* Working proficiency with Python 3. If you can read it and follow the program, you should be okay.

[Lab 0](./00-prerequisites/) walks you through the setup if you need help!

## Labs

- [Lab 0](#00---prerequisites)
- [Intro](#interlude-a-crash-course-in-clouds)
- [Lab 1](#01---infrastructure-basics)
- [Lab 2](#02---adding-applications)
- [Lab 3](#03---cloud-hopping)
- [Lab 4](#04---bonus-abstractions-and-platform-engineering)

### 00 - Prerequisites

_Time: 15 min to 1 hour_<br/>
[Lab 00](./00-prerequisites/)

Before getting started, you need to have a few things set up. The [prerequisites lab](./00-prerequisites/) walks you through each piece step by step.

### Interlude: A crash course in clouds

_Time: 20 min_

Before we dive into the code, we'll talk about cloud-based infrastructures and the differences among various cloud providers. We'll explore why Infrastructure as Code (IaC) is helpful here and what cloud engineering is. We'll also talk about clouds---the fluffy kind!

### 01 - Infrastructure Basics

_Time: 1.5 hour_<br/>
[Lab 01](./lab-01/)

Then we'll put together our first set of infrastructure on a public cloud, GCP, building the skeleton of our first scientific computing lab. [Check out the lab](./lab-01/).

### Interlude: Break

_Time: 10 min_

Between lab 1 and lab 2, we'll take a short break to stretch, grab a drink, and do anything else necessary before diving back in.

### 02 - Adding Applications

_Time: 30 min to 1 hour_<br/>
[Lab 02](./lab-02/)

For lab 2, we'll add in our first analytics program with pandas. [Explore the lab](./lab-02/).

### 03 - Cloud Hopping

_Time: 1 hour_<br/>
[Lab 03](./lab-03/)

In lab 3, we'll start hopping over to another cloud, AWS. We'll learn about the constraints of AWS versus GCP, and we'll figure out how to think more in terms of components to get around the different business philosophies of each cloud when thinking about citizen science. [Check out the lab](./lab-03/).

### 04 - BONUS: Abstractions and Platform Engineering

_Time: 1 hour_</br>
[Lab 04](./lab-04/)

If we have time, we'll dive into lab 4! We'll start building up our abstractions of different infrastructure components to make it easier to hop from cloud to cloud with our existing code. Also, we'll explore how our app code needs to change to move to another cloud. Note that this part of the lab might stray from the free tier, which is why it's a bonus lab :) [Check out the lab](./lab-04/).
