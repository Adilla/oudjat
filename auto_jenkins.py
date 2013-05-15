from jenkins import Jenkins
import sys, os


def create_jenkins_job(config_path, job_name):
    """ 
    Create new job with new config file
    """
    
    f = open(config_path, "r")
    str_config = ''
    for line in f:
        str_config = str_config + line
            
    j = Jenkins('http://localhost:8080')
    
    if j.job_exists(job_name) == False:
        j.create_job(job_name, str_config)



def create_jenkins_job(init_job_config, job_name):
    """
    Create new job by getting config file 
    from existing job
    """

    j = Jenkins('http://localhost:8080')

    str_config = j.get_job_config(init_job_config)

    if j.job_exists(job_name) == False:
        j.create_job(job_name, str_config)
    


if __name__ == "__main__":

    try:
        create_jenkins_job(sys.argv[1], sys.argv[2])
    except:
        if len(sys.argv) != 2:
            sys.stdout.write("Incorrect number of arguments\n")
            sys.stdout.write("python auto_jenkins.py <config path> <new job name>\n")
            sys.stdout.write("python auto_jenkins.py <existing job name> <new job name>\n")

    

