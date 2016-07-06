#!/bin/bash

# Simple wrapper for a MetaMap pipeline.
# Expects input on STDIN, writes to STDOUT.

# NOTE: this script assumes MetaMap 2011 and requires that
# the MetaMap support services are running. If you have
# MetaMap installed in $MM, these can be started as
#
#    $MM/bin/skrmedpostctl start
#    $MM/bin/wsdserverctl start

METAMAP_ROOT=~/Tools/MetaMap

# -N specifies "fielded" output and is assumed by tools using this script
# -J specifies restriction to the given UMLS semantic types
#METAMAP_ARGS="-N -J anab,anst,bdsu,bdsy,blor,bpoc,bsoj,celc,cell,emst,ffas,tisu"
METAMAP_ARGS="-N -J aapp,acab,aggp,anab,anst,antb,arch,bacs,bact,bdsu,bdsy,bhvr,biof,blor,bmod,bodm,bpoc,bsoj,cgab,chem,chvf,chvs,clna,clnd,cnce,comd,diap,drdd,dsyn,emod,emst,enzy,euka,famg,ffas,fndg,hlca,hops,horm,imft,inch,inpo,irda,lang,lbpr,lbtr,lipd,medd,menp,mobd,moft,neop,nnon,npop,nsba,orch,orga,orgf,ortf,patf,qlco,rcpt,resa,resd,sbst,sosy,spco,strd,tisu,tmco,topp,virs,vita"


$METAMAP_ROOT/public_mm/bin/metamap13 $METAMAP_ARGS $@

