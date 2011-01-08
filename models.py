from django.db import models
from django.db import connection

class Report(models.Model):
    name = models.CharField(max_length=255)
    query = models.TextField()
    totals_query = models.TextField(blank=True, null=True)

    """    
    def save(self, *args, **kwargs):
        super(Puzzle, self).save(*args, **kwargs)
        self.puzzlepiece_set.all().delete()
        self.create_pieces()
        super(Puzzle, self).save(*args, **kwargs)
    """        
    
PARAMETER_TYPES = (
    ('DATETIME', 'Date/Time'),
    ('DROPDOWNLIST', 'Predefined List'),
    ('DROPDOWNLISTFROMQUERY', 'Query Results List'),
    ('TEXT', 'Text'),
)    
    
class ReportParameter(models.Model):
    report = models.ForeignKey(Report)
    parameter_type = models.CharField(max_length=255, choices=PARAMETER_TYPES)
    label = models.CharField(max_length=255)
    list_items = models.TextField(blank=True, default='')
    default_value = models.CharField(max_length=255, blank=True, default='')
        
    def is_dropdown_list(self):
        return self.parameter_type in ('DROPDOWNLIST', 'DROPDOWNLISTFROMQUERY',)
    
    def get_list_items(self):
        if self.parameter_type == 'DROPDOWNLIST':
            output = ['',] + [i.strip() for i in self.list_items.split('\n')]
            return ((item,item) for item in output)
        elif self.parameter_type == 'DROPDOWNLISTFROMQUERY':
            from django.db import connection
            cursor = connection.cursor()
            try:
                cursor.execute(self.list_items)
            except Exception as ex: 
                print 'An error occurred getting the list items from a query: %s' % ex
                return ''
            output = [('','')]
            results = cursor.fetchall()
            for item in results:
                if len(item) > 1:
                    output.append((item[0], item[1]))
                elif len(item) == 1:
                    output.append((item[0], item[0]))
            return (item for item in output)
        return ''
