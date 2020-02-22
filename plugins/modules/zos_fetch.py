# -*- coding: utf-8 -*-
# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}


DOCUMENTATION = r'''
---
module: zos_fetch
version_added: 1.0
short_description: Fetches data from remote z/OS system to local machine
description:
  - The M(zos_fetch) module copies a file on the z/OS system to the local machine. 
    Use the M(zos_copy) module to copy files from local machine to the remote z/OS system.
author: Asif Mahmud <asif.mahmud@ibm.com>
options:
  src:
    description:
      - Name of PDS, PDS(E) members, VSAM data set, USS file path
    required: true
  dest:
    description:
      - Local path where the file or data set will be stored
    required: true
  is_catalog:
    description:
      - Specifies if the data set is cataloged. When trying to fetch an 
        uncataloged data set, this parameter must be set to false and the 
        volume where the data set is stored must be provided. Default is true.
    required: false
    default: "true"
    choices: [ "true", "false" ]
  volume:
    description:
      - Name of the volume when I(is_catalog=false)
    required: false
  fail_on_missing:
    description:
      - When set to true, the task will fail if the source file is missing. 
        If the data set is uncataloged and I(is_catalog=false), then the task 
        will not fail and will attempt to fetch the uncataloged data set.
    required: false
    default: "false"
    choices: [ "true", "false" ]
  validate_checksum:
    description:
      - Verify that the source and destination checksums match after the files are fetched. 
    required: false
    default: "true"
    choices: [ "true", "false" ]
  flat: 
    description:
      - Override the default behavior of appending
        hostname/path/to/file to the destination. If dest ends with '/', it
        will use the basename of the source file, similar to the copy module.
        Obviously this is only handy if the filenames are unique.
    required: false
    default: "true"
    choices: [ "true", "false" ]
  is_binary:
    description:
      - Specifies if the file being fetched is a binary
    required: false
    default: "false"
    choices: [ "true", "false" ]
  is_vsam:
    description:
      - Indicates whether the data set to be fetched is a VSAM data set. If I(is_vsam=true), 
        it uses the IDCAMS utility to copy the VSAM data into a temporary data set, which is 
        then fetched to the local machine. The temporary data set is deleted afterwards.
    required: false
    default: "false"
    choices: ["true", "false" ]
  encoding:
    description:
      - The encoding of the existing file or data set on the remote z/OS system.
        Setting the value to "ASCII" will not convert the encoding before transfer,
        whereas the default value of "EBCDIC" will convert the encoding of the file
        or data set to ASCII before transfer. Note that the conversion to ASCII does
        not affect the existing file or data set.
    required: false
    default: "EBCDIC"
    choices: ["ASCII", "EBCDIC" ]
  is_uss: 
    description:
      - Specifies if the file to be fetched resides on the Unix System Services
    required: false
    default: "false"    
    choices: [ "true", "false" ]
  use_qualifier:
    description:
      - Indicates whether the data set high level qualifier should be used when fetching
    required: false
    default: "false"
    choices: [ "true", "false" ]
  wait_s:
    description:
      - The time (in seconds) to wait for an uncataloged data set to be recataloged
    required: false
    default: 10
    type: int
notes:
    - When fetching PDS(E) and VSAM data sets, temporary storage will be used on the remote
      z/OS system. After the PDS(E) or VSAM data set is successfully transferred, the temprorary
      data set will deleted. The size of the temporary storage will correspond to the size of
      PDS(E) or VSAM data set being fetched. If module executation fails, the temporary storage 
      will be cleaned.
    - To prevent redundancy, additional checksum validation will not be done when fetching PDS(E) 
      because data integrity checks are done through the transfer methods used. As a result, the module 
      response will not include C(checksum) parameter. 
'''

EXAMPLES = r'''
- name: Fetch file from USS and store into /tmp/fetched/host.example.com/tmp/somefile
  zos_fetch:
    src: /tmp/somefile
    dest: /tmp/fetched
    is_uss: true

- name: Fetch a sequential data set and store in /tmp/SOME.DATA.SET
  zos_fetch:
    src: SOME.DATA.SET
    dest: /tmp/
    flat: true

- name: Fetch a PDS as binary and store in /tmp/SOME.PDS.DATASET
  zos_fetch:
	src: SOME.PDS.DATASET
	dest: /tmp/
	flat: true
	is_binary: true

- name: Fetch a unix file without converting from EBCDIC to ASCII. Fail if file is missing
  zos_fetch:
    src: /tmp/somefile
    dest: /tmp/
    is_uss: true
	encoding: ASCII
	fail_on_missing: true

- name: Fetch a unix file and don't validate its checksum. Fail if the file is missing
  zos_fetch:
    src: /tmp/somefile
    dest: /tmp/
    flat: true
    validate_checksum: false
    is_uss: true
    fail_on_missing: true

- name: Fetch an uncataloged VSAM data set
  zos_fetch:
    src: USER.TEST.VSAM
    dest: /tmp/
    flat: true
    is_vsam: true
    is_catalog: false
    volume: SCR03
    wait_s: 15

- name: Fetch a PDS member named 'data'
  zos_fetch:
    src: USER.TEST.PDS(data)
    dest: /tmp/
    flat: true

- name: Fetch an uncataloged sequential data set
  zos_fetch:
    src: USER.TEST.SEQ
    dest: /tmp/
    flat: true
    is_catalog: false
    volume: SCR03
    wait_s: 5
'''

RETURNS = r'''
file:
	description: The source file path on remote machine
	returned: success
	type: str
	sample: SOME.DATA.SET
dest: 
	description: The destination file path on controlling machine
	returned: success
	type: str
	sample: /tmp/SOME.DATA.SET
transfer_mode:
	description: Indicates which transfer mode was used to fetch the file (binary or text)
	returned: success
	type: str
	sample: binary
encoding:
	description: The encoding of the fetched file
	returned: success
	type: str
	sample: ascii
checksum:
	description: The SHA1 checksum of the fetched file
	returned: success
	type: str
	sample: 33ab5639bfd8e7b95eb1d8d0b87781d4ffea4d5d
data_set_type:
	description: Indidcates the fetched file's data set type
	returned: success
	type: str
	sample: PDSE
rc:
    description: The return code returned by a process executed on the remote z/OS system
    returned: failure
    type: str
    sample: 12
stdout:
    description: The stdout of a command executed on the target z/OS system
    returned: failure
    type: str
    sample: DATA SET 'USER.PROCLIB' NOT IN CATALOG
stderr:
    description: The stderr of a command executed on the target z/OS system
    returned: failure
    type: str
    sample: TypeError: 'int' object is not callable
'''


import os
import base64
import subprocess
import hashlib
import random
import string
import re
import tempfile
import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes
from ansible.module_utils.parsing.convert_bool import boolean
from zoautil_py import Datasets, MVSCmd
from zoautil_py import types


# Ansible module object
module = None

MVS_DS_TYPES = frozenset({'PS', 'PO', 'PDSE', 'PE'})


def _fail_json(**kwargs):
    """ Wrapper around AnsibleModule.fail_json """
    module.fail_json(**kwargs)

def _run_command(cmd, **kwargs):
    """ Wrapper around AnsibleModule.run_command """
    return module.run_command(cmd, **kwargs)

def _fetch_uss_file(src, validate_checksum, is_binary):
    """ Read a USS file and return its contents """
    read_mode = 'rb' if is_binary else 'r'
    content = checksum = None
    try:
        with open(src, read_mode) as infile:
            content = infile.read()
            if is_binary:
                content = base64.b64encode(content)
            
            if validate_checksum:
                checksum = _get_checksum(content)
   
    except (FileNotFoundError, IOError, OSError) as err:
        _fail_json(msg=str(err))
    
    return content, checksum

def _fetch_zos_data_set(zos_data_set, is_binary, fetch_member=False):
    """ Read a sequential data set and return its contents """
    if fetch_member:
        rc, out, err = _run_command("cat \"//'{}'\"".format(zos_data_set))
        if rc != 0:
            _fail_json(msg="Failed to read data set member for data set {}".format(zos_data_set), rc=rc, stdout=out, stderr=err)
        content = out
    else:
        content = Datasets.read(zos_data_set)
    
    if is_binary:
        content = content.encode('utf-8', 'surrogateescape').decode('utf-8', 'replace')
        return base64.b64encode(content.encode())
    return content

def _create_temp_data_set_name(LLQ):
    """ Create a temporary data set name """
    chars = string.ascii_uppercase
    HLQ2 = ''.join(random.choice(chars) for i in range(5))
    return Datasets.hlq() + '.' + HLQ2 + '.' + LLQ

def _copy_vsam_to_temp_data_set(ds_name):
    """ Copy VSAM data set to a temporary sequential data set """
    sysin = _create_temp_data_set_name('SYSIN')
    out_ds = _create_temp_data_set_name('OUTPUT')
    sysprint = _create_temp_data_set_name('SYSPRINT')

    Datasets.create(sysin, 'SEQ')
    Datasets.create(out_ds, 'SEQ')
    Datasets.create(sysprint, "SEQ", "", "FB", "",133)

    repro_sysin = ' REPRO INFILE(INPUT)  OUTFILE(OUTPUT) '
    Datasets.write(sysin, repro_sysin)

    dd_statements = []
    dd_statements.append(types.DDStatement(ddName='sysin', dataset=sysin))
    dd_statements.append(types.DDStatement(ddName='input', dataset=ds_name))
    dd_statements.append(types.DDStatement(ddName='output', dataset=out_ds))
    dd_statements.append(types.DDStatement(ddName='sysprint', dataset=sysprint))

    try:
        rc = MVSCmd.execute_authorized(pgm='idcams', args='', dds=dd_statements)
    except Exception as err:
        if Datasets.exists(out_ds):
            Datasets.delete(out_ds)
        
        if rc != 0:
            _fail_json(msg="Non-zero return code received while executing MVSCmd to copy VSAM data set {}".format(ds_name), rc=rc)
        
        _fail_json(msg="Failed to call IDCAMS to copy VSAM data set {} to sequential data set: {}".format(ds_name, str(err)))

    finally:
        Datasets.delete(sysprint)
        Datasets.delete(sysin)

    return out_ds

def _fetch_vsam(src, validate_checksum, is_binary):
    """ Fetch a VSAM data set """
    checksum = None
    temp_ds = _copy_vsam_to_temp_data_set(src)
    content = _fetch_zos_data_set(temp_ds, is_binary)
    if content is None:
        content = ''
    
    rc = Datasets.delete(temp_ds)
    if rc > 0:
        _fail_json(msg="Unable to delete data set {}".format(temp_ds))
    
    if validate_checksum:
        checksum = _get_checksum(content)
    
    return content, checksum

def _recatalog_data_set(ds_name, volume, vsam=False):
    """ Recatalog an uncataloged data set """
    sysin_ds_name = _create_temp_data_set_name('SYSIN')
    Datasets.create(sysin_ds_name, 'SEQ')

    if vsam:
        idcams_sysin = ''' DEFINE CLUSTER -
            (NAME({}) -
            VOLUME({}) -
            RECATALOG) '''.format(ds_name, volume)
    else:
        idcams_sysin = ''' DEFINE NVSAM -
            (NAME({}) -
            VOLUMES({}) - 
            DEVT(SYSDA)) '''.format(ds_name, volume)

    Datasets.write(sysin_ds_name, idcams_sysin)
    dd_statements = []
    dd_statements.append(types.DDStatement(ddName="sysin", dataset=sysin_ds_name))
    dd_statements.append(types.DDStatement(ddName="sysprint", dataset='*'))

    try:
        rc = MVSCmd.execute_authorized(pgm="idcams", args='', dds=dd_statements)
        if rc != 0:
            _fail_json(msg="Non-zero return code received while executing MVSCmd to recatalog {}".format(ds_name), rc=rc)
    
    except Exception as err:
        _fail_json(msg="Failed to call IDCAMS to recatalog data set {}: {}".format(ds_name, str(err)))
    
    finally:
        Datasets.delete(sysin_ds_name) 

    return ds_name

def _uncatalog_data_set(ds_name, vsam=False):
    """ Uncatalog a data set """
    if vsam:
        cmd = "tsocmd \"DELETE '{}' CLUSTER NOSCRATCH NOPURGE\"".format(ds_name)
    else:
        cmd = "tsocmd \"ALLOC DA('{}') REUSE OLD UNCATALOG\"".format(ds_name)
    
    rc, out, err = _run_command(cmd)
    if rc != 0:
        _fail_json(msg="Unable to uncatalog data set {}".format(ds_name), rc=rc, stdout=out, stderr=err)

def _convert_from_ebcdic_to_ascii(data):
    """ Convert encoding from EBCDIC to ASCII """
    rc, out, err = _run_command("iconv -f IBM-1047 -t ISO8859-1", data=data)
    if rc != 0:
        _fail_json(msg="Unable to convert from EBCDIC to ASCII", rc=rc, stdout=out, stderr=err)
    return out

def _get_checksum(data):
    """ Calculate checksum for the given data """
    digest = hashlib.sha1()
    data = to_bytes(data, errors='surrogate_or_strict')
    digest.update(data)
    return digest.hexdigest()

def _determine_data_set_type(ds_name):
    """ Use the LISTDS utility to determine the type of a given data set """
    rc, out, err = _run_command("tsocmd \"LISTDS '{}'\"".format(ds_name))

    if "NOT IN CATALOG" in out:
        raise UncatalogedDatasetError(ds_name)

    if "INVALID DATA SET NAME" in out:
        if os.path.exists(ds_name) and os.path.isfile(ds_name):
            return 'USS'
        _fail_json(msg="The file {} does not exist".format(ds_name))
    
    if rc != 0:
        msg = None
        if "ALREADY IN USE" in out:
            msg = "Dataset {} may already be open by another user. Close the dataset and try again.".format(ds_name)
        else:
            msg = "Unable to determine data set type for data set {}.".format(ds_name)
        _fail_json(msg=msg, rc=rc, stdout=out, stderr=err)
    
    ds_search = re.search("(-|--)DSORG(|-)\n(.*)", out)
    if ds_search:
        return ds_search.group(3).split()[-1].strip()
    return None

def _fetch_pdse(src):
    """ Fetch a partitioned data set """
    result = dict()
    temp_dir = tempfile.mkdtemp()    
    rc, out, err = _run_command("cp \"//'{}'\" {}".format(src, temp_dir))
    if rc != 0:
        _fail_json(msg="Error copying partitioned data set to USS", rc=rc, stdout=out, stderr=err)
    
    result['pds_path'] = temp_dir
    return result

def _fetch_ps(src, validate_checksum, is_binary):
    """ Fetch a sequential data set """
    checksum = None
    content = _fetch_zos_data_set(src, is_binary)
    if not content:
        _fail_json(msg="Error fetching sequential data set {}".format(src))
    if validate_checksum:
        checksum = _get_checksum(content)
    return content, checksum

def _validate_dsname(ds_name):
    """ Validate the name of a given data set """
    dsn_regex = "^(([A-Z]{1}[A-Z0-9]{0,7})([.]{1})){1,21}[A-Z]{1}[A-Z0-9]{0,7}$"
    return re.match(dsn_regex, ds_name[:ds_name.find('(')]) 

def _validate_params(src, is_binary, encoding, is_catalog, volume, is_uss, _fetch_member):
    """ Ensure the module parameters are valid """ 
    msg = None
    if is_binary and encoding is not None:
        msg = "Encoding parameter is not valid for binary transfer"
    if encoding and (encoding != 'EBCDIC' and encoding != 'ASCII'):
        msg = "Invalid value supplied for 'encoding' option, it must be either EBCDIC or ASCII"
    if not is_catalog  and not volume:
        msg = "Volume not provided for uncataloged data set"
    if not is_uss and not _validate_dsname(src):
        msg = "Invalid data set name provided"

    if msg:
        _fail_json(msg=msg)


def run_module():
    global module
    module = AnsibleModule(
        argument_spec = dict(
            src                 = dict(required=True, type='path'),
            dest                = dict(required=True, type='path'),
            is_catalog          = dict(required=False, default=True, type='bool'),
            volume              = dict(required=False, type='str'),
            fail_on_missing     = dict(required=False, default=False, choices=[True, False], type='str'),
            validate_checksum   = dict(required=False, default=True, choices=[True, False], type='str'),
            flat                = dict(required=False, default=True, choices=[True, False], type='str'),
            is_binary           = dict(required=False, default=False, type='bool'),
            is_vsam             = dict(required=False, default=False, type='bool'),
            encoding            = dict(required=False, choices=['ASCII', 'EBCDIC'], type='str'),
            is_uss              = dict(required=False, default=False, type='bool'),
            wait_s              = dict(required=False, default=10, type='int'),
            use_qualifier       = dict(required=False, default=False, type='bool'),
            _fetch_member       = dict(required=False, type='bool')
        )
    )

    src                 = module.params.get('src', None)
    b_src               = to_bytes(src)
    encoding            = module.params.get('encoding')
    volume              = module.params.get('volume')
    wait_s              = module.params.get('wait_s') 
    fail_on_missing     = boolean(module.params.get('fail_on_missing'), strict=False)
    validate_checksum   = boolean(module.params.get('validate_checksum'), strict=False)
    is_uss              = boolean(module.params.get('is_uss'), strict=False)
    is_binary           = boolean(module.params.get('is_binary'), strict=False)
    is_vsam 	        = boolean(module.params.get('is_vsam'), strict=False)
    is_catalog          = boolean(module.params.get('is_catalog'), strict=False)
    use_qualifier       = boolean(module.params.get('use_qualifier'), strict=False)
    _fetch_member       = boolean(module.params.get('_fetch_member'), strict=False)

    _validate_params(src, is_binary, encoding, is_catalog, volume, is_uss, _fetch_member)

    res_args = dict()
    if (not is_uss or '/' not in src) and use_qualifier:
        src = Datasets.hlq() + '.' + src
    
    ds_name = src if not _fetch_member else src[:src.find('(')]
    
    try:
        ds_type = _determine_data_set_type(ds_name)
    
    except UncatalogedDatasetError as err:
        if is_catalog or fail_on_missing:
            _fail_json(msg=str(err))
    
        _recatalog_data_set(ds_name, volume, vsam=is_vsam)
        time.sleep(wait_s)
        ds_type = _determine_data_set_type(ds_name)
        if not ds_type:
            _fail_json(msg="Could not determine data set type") 
    

    if ds_type in MVS_DS_TYPES and not Datasets.exists(src):
        res_args['msg'] = "The MVS data set {} does not exist".format(src)
        
    elif ds_type == 'USS' and not os.path.exists(b_src):
        res_args['msg'] = "The file {} does not exist".format(src)
        
    if res_args.get('msg'):
        if fail_on_missing:
            _fail_json(**res_args)
        module.exit_json(**res_args)

    # Fetch sequential dataset
    if ds_type == 'PS':
        content, checksum = _fetch_ps(src, validate_checksum, is_binary)
        res_args['checksum'] = checksum
        res_args['content'] = content

    # PDS/PDSE
    elif ds_type in ('PO', 'PDSE', 'PE'):
        if _fetch_member:
            content = _fetch_zos_data_set(src, is_binary, fetch_member=True)
            res_args['content'] = content
            res_args['checksum'] = _get_checksum(content)
        else:
            result = _fetch_pdse(src)
            res_args['pds_path'] = result['pds_path']

    # USS file
    elif is_uss:
        content, checksum = _fetch_uss_file(src, validate_checksum, is_binary)
        res_args['checksum'] = checksum
        res_args['content'] = content

    # VSAM dataset
    elif is_vsam:
        content, checksum = _fetch_vsam(src, validate_checksum, is_binary)
        res_args['checksum'] = checksum
        res_args['content'] = content

    if not is_catalog:
        _uncatalog_data_set(ds_name, vsam=is_vsam)
    
    res_args['file'] = src
    res_args['ds_type'] = ds_type
    module.exit_json(**res_args)



class UncatalogedDatasetError(Exception):
    def __init__(self, ds_name):
        super().__init__("Data set {} is not in catalog. If you would like to fetch the data set, please specify its volume".format(ds_name))

def main():
    run_module()


if __name__ == '__main__':
    main()