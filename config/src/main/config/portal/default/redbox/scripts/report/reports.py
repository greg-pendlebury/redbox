from java.util import Date
from java.util import Calendar
from java.lang import String
from com.googlecode.fascinator.common import JsonObject
from com.googlecode.fascinator.portal.report import RedboxReport
from org.apache.commons.io import FileUtils
from java.io import File
from com.googlecode.fascinator.common import FascinatorHome

class ReportsData:

    def __init__(self):
        pass
    def __activate__(self, context):
        self.auth = context["page"].authentication
        self.errorMsg = "" 
        self.request = context["request"]
        self.response = context["response"]
        self.formData = context["formData"]
        self.log = context["log"]
        self.reportManager = context["Services"].getService("reportManager")
            
        if (self.auth.is_logged_in()):
            if (self.auth.is_admin()==True):
                pass
            else:
                self.errorMsg = "Requires Admin / Librarian / Reviewer access." 
        else:
            self.errorMsg = "Please login."
        if self.errorMsg == "": 
            
            self.func = self.formData.get("func", "")
            if self.func == "" and self.request.getParameter("func"):
                self.func = self.request.getParameter("func")
            
            if self.func == "action":
                self.action = self.request.getParameter("action")
                if self.action == "create":
                    self.createReport()
                    out = self.response.getPrintWriter("text/plain; charset=UTF-8")
                    out.println("{\"id\":\""+String(self.formData.get("reportName")).replaceAll(" ","")+"\"}")
                    out.close()
                if self.action == "options":
                    out = self.response.getPrintWriter("text/plain; charset=UTF-8")
                    out.println(FileUtils.readFileToString(File(FascinatorHome.getPath("reports")+"/reportCriteriaOptions.json")))
                    out.close()
                    return   
                    
        
    def createReport(self):
        self.report = RedboxReport(String(self.formData.get("reportName")).replaceAll(" ",""),self.formData.get("reportName")) 
        self.report.setQueryFilterVal("dateFrom",self.formData.get("dateFrom"),"dateFrom", "dateFrom")
        self.report.setQueryFilterVal("dateTo",self.formData.get("dateTo"),"dateTo", "dateTo")
        
        for fieldName in self.formData.getFormFields():
            if fieldName != "reportName":
                self.report.setQueryFilterVal(fieldName,self.formData.get(fieldName),fieldName, fieldName)           
        
        self.reportManager.addReport(self.report)
        self.reportManager.saveReport(self.report)
       
        
    
    def getErrorMsg(self):
        return self.errorMsg
            
    def buildDashboard(self, context):
        self.velocityContext = context
               
    def getFromDt(self):
        return self.fromDtTxt
    
    def getToDt(self):
        return self.toDtTxt
    
    def getDateRange(self):
        return "from="+ self.getFromDt() + "&to=" + self.getToDt()
           
    