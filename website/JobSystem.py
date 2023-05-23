from .models import *
from .ImageManager import ImageManager
from . import db
from .SingletonMeta import SingletonMeta


class JobSystem(metaclass=SingletonMeta) :
    def __init__(self , db) -> None:
        self.db = db

    def PostJob(self , job :Job , img : None ):
        self.db.session.add(job)
        self.db.session.commit()
        if img != None :
            fname = ImageManager.SaveImage(img , job)
            if fname == None :
                print("Error in saving image")
                self.db.session.delete(job)
                self.db.session.commit()
                return False
            
            job_image = JobImage(job_id = job.id , image_path = fname)
            self.db.session.add(job_image)
            self.db.session.commit()
        return True
    

    def GetAllJobs(self) -> list[Job]:
        print("Getting all jobs")
        return Job.query.all()
        
    def GetJob(self , id) -> Job:
        return Job.query.get_or_404(id)

    def ApplyForJob(self , job_id , user_id) -> bool  :
        print("Applying for a job")
        try :
            job = Job.query.get(job_id)
            user = User.query.get(user_id)
            if not job or not user :
                print("User or job not found")
                return False
            job_application = JobApplication(job_id = job_id , user_id = user_id , job_status = 'Pending')
            self.db.session.add(job_application)
            self.db.session.commit()
            return True
        except:
            print("Error in applying for job")
            return False
            
        
    def GetJobImage(self , job_id : int) -> JobImage:
        """ 
        Args:
            job_id (int): _description_

        Returns:
            JobImage: 
        """        
        return JobImage.query.filter_by(job_id = job_id).first()

    def DeleteJob(self , id : int , owner_id) -> bool:
        """ 
        Delete a job from the database.
        Args:
            id (int): id of the job
            owner_id (int) : id of the owner
        
        Returns:
            bool: True if job deleted else False.
        """        
        
        try:
            job = Job.query.get(id)
            if job.user_id != owner_id :
                print("User not authorized to delete job")
                return False
            self.db.session.delete(job)
            self.db.session.commit()
            return True
        except:
            return False

    def GetPostedJobs(self , user_id : int) -> list[Job] :
        """ 
        Get all the jobs posted by a user.
        Args:
            user_id (int): id of the user

        Returns:
            list: list of jobs.
        """        
        return Job.query.filter_by(user_id = user_id).all()

    def GetAppliedJobs(self , user_id : int) -> list[Job]:
        """ 
        Get all the jobs applied by a user.
        Args:
            user_id (int): id of the user

        Returns:
            list: list of jobs.
        """        
        applications =  JobApplication.query.filter_by(user_id = user_id).all()

        # ge the jops corresponding to the applications
        jobs = []
        for application in applications :
            job = Job.query.get(application.job_id)
            if job :
                jobs.append(job)
        
        return jobs
        
    def GetJobApplications(self , job_id : int) -> list[JobApplication]:
        """ 
        Get all the applications for a job.
        Args:
            job_id (int): id of the job

        Returns:
            list: list of applications.
        """        
        return JobApplication.query.filter_by(job_id = job_id).all()
        

    

jobSystem = JobSystem(db)