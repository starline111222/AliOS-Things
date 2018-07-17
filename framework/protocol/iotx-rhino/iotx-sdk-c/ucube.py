import commands
import os,sys,subprocess
import shutil

name = 'iotx-sdk-c'

def build_function(output_dir, component):
    config_file = "framework/protocol/iotx-rhino/iotx-sdk-c/aos_board_conf.mk"
    print( "Making config file "+ config_file )
    with open( config_file, 'w') as f:
        f.write("#------ this file is auto generated by scons ------#\n")
        flag_str = " ".join(aos_global_config.cflags)
        f.write( "CONFIG_ENV_CFLAGS += " + flag_str + "\n" )
        f.write( "CROSS_PREFIX := " + aos_global_config.toolchain.prefix + "\n")
    
    
    targets=['libiot_sdk.a']
    output_targets=[]
    for target in targets:
        output_targets.append( output_dir+"/"+ target )
      
    print( 'making '+name )
    
    origin_path=os.getcwd();
    os.chdir('framework/protocol/iotx-rhino/iotx-sdk-c/')
      
    try:
        cmd='make distclean'
        log = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        print( log )
        cmd='make prune'
        log = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        print( log )
        cmd='make'
        log = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        print( log )
    except subprocess.CalledProcessError as e:
        log = e.output+"\n"     
        print( 'component ' + name + 'build failed!' )
        print( log )
        sys.exit(1)
            
    os.chdir(origin_path)
    
    
    #copy targets
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for target in targets:
        shutil.copy( component.dir+"/output/release/lib/"+target,  output_dir)


    print( name+' make over~' )
    return output_targets    
    
component = aos_self_build_component( name, build_function )

global_includes =Split(''' 
    src/sdk-impl
    src/utils/digest
    src/utils/misc
    src/sdk-impl/exports
    src/utils/log
    src/sdk-impl/imports
    src/services/linkkit/dm
''')

for i in global_includes:
    component.add_global_includes(i)

    
