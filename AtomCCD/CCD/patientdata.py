from  ccdaparser import json_data



class Demographics:

      """Holds patients demographics information"""
      
      def __init__(self):
            self.demo_data = json_data['demographics']
            self.keys = self.demo_data.keys()
      def name(self):
          """Return patient's given and family names
             Keys to use : 'given' for first name
                         : 'family' for last name'
                         : 'prefix' for title'
             

          """
          return self.demo_data.get('name','name not found')

      def address(self):
          
        """Return patient's address
             Keys to use : 'city','state','street', 'country', zip       

        """
        return self.demo_data.get('address','address not found')


      def gender(self):

        """Return patient's gender(Male or Female)
             Keys to use : no keys needed        

        """
        return self.demo_data('gender','no gender assigned')


      def dob(self):
                   
        """Return patient's date of birth as mm/dd/yyyy
             Keys to use : no keys needed        

        """
        return self.demo_data('gender','no gender assigned')

      def provider(self):
        """Return patient's provider information
             Keys to use : no keys needed        

        """
        return self.demo_data.get('provider','no provider information was found')


      def __repr__(self):
         """ The following list of useful methods can be called in Demographics instances"""
         for key in self.keys:
             print key
         return "The program supports only subset of the above methods as of Oct 31,2014"

      
                   
                   
                   



demo = Demographics()
print demo
           
           
