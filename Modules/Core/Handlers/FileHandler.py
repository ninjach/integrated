import os
import pandas as pd

class FileHandler(object):

    """
    Handles files for all modules
    """

    def __init__(self):
        """
        TODO: 
            Load input/output folder paths from config
            Define file loader functions (load irrigation files, load storage files, etc.)
        """
        pass

    #End init()

    def getFolders(self, folder):
        """
        Get a list of folders within the target folder

        :Returns: list of (relative) paths
        """

        folder_list = []
        for f in os.listdir(folder):

            f = folder+'/'+f
            if os.path.isdir(f):
                folder_list.append(f)
            #End if
        #End for

        return folder_list

    #End getFolders()


    def getFileList(self, folder, ext=".csv", walk=True):

        """
        Get a list of files with the matching extension in the given folder.

        :param folder: Path of folder to search
        :param ext: File extension to look for
        :param walk: (True | False) Search subfolders found within :folder:
        :returns: A list of files

        """

        file_list = []

        if walk is True:
            for root, dirs, files in os.walk(folder):
                for f in files:
                    if f.endswith(ext):
                        file_list.append(os.path.join(root, f))
                    #End if
                #End for
            #End for
        else:
            for f in os.listdir(folder):
                if f.endswith(ext):

                    f = folder+'/'+f
                    file_list.append(f)
                #End if
            #End for

        return file_list

    #End getFileList()

    def importFiles(self, folder, ext=".csv", walk=False, date_range=None, **kwargs):

        """
        Import files found within a given folder into Pandas DataFrame

        WARNING: Matching folder and file combinations will overwrite each other.

        :param folder: Folder to search
        :param ext: File extension to search for
        :param walk: (True | False) search subfolders in the given folder
        :param date_range: If data is a time series, date range to extract; index must be set for this to work
        :param kwargs: Other arguments accepted by Pandas read_csv()
        :returns: Dict of Pandas DataFrame for each file found

        """

        imported = {}

        files = self.getFileList(folder, ext, walk)

        for f in files:
            fname = os.path.splitext(f)[0] #Get filename without extension
            
            path, fname = os.path.split(fname) #Get filename by itself

            #Get parent directory of file
            parent_dir = os.path.basename(path)

            if parent_dir not in imported:
                imported[parent_dir] = {}

            try:
                imported[parent_dir][fname] = pd.read_csv(f, **kwargs)
            except ValueError as e:
                print "Error occured while trying to import {}".format(f)

            if date_range is not None:
                start = date_range[0]
                end = date_range[1]

                temp = imported[parent_dir][fname]

                if start is not None:
                    temp = temp[temp.index >= pd.to_datetime(start)]

                if end is not None:
                    temp = temp[temp.index <= pd.to_datetime(end)]

                if start is not None:
                    imported[fname] = temp[temp.index >= pd.to_datetime(start)]

                if end is not None:
                    imported[fname] = temp[temp.index <= pd.to_datetime(end)]
            #End if

        #End for

        return imported

    #End importFile()

    def loadCSV(self, filepath, columns=None, **kwargs):

        """
        Load data from CSV file.

        This may look like a useless wrapper around a Pandas function.
        It is defined here so that inheriting Classes may modify as appropriate while keeping the same function name

        :param filepath: name of file to import
        :param columns: a list of column headers (as found in the file) to return. Returns all if None
        :param kwargs: Other arguments accepted by Pandas read_csv()
        :returns: Pandas DataFrame

        """

        return pd.read_csv(filepath, usecols=columns, **kwargs)
        
    #End loadData()

    def setupDir(self, folder_path):

        """
        WARNING: ONLY SET UP FOR WINDOWS SYSTEMS
        WILL NOT CHECK FOR ERRORS ON UNIX-LIKE SYSTEMS
        """

        if folder_path[-1] != "/":
            output_path = folder_path+"/"

        if os.path.exists(os.path.dirname(output_path)) is False:

            try:
                os.makedirs(os.path.dirname(output_path))
            except WindowsError as e:
                print e
                pass
            #End try catch
        #End if

        return output_path
    #End setupDir

    def writeCSV(self, df, filepath, filename, **kwargs):

        """
        Write out a DataFrame to CSV

        :param df: DataFrame to export
        :param filepath: name and location of where to export the csv file to
        :param kwargs: Other arguments accepted by Pandas read_csv()
        :returns: CSV string (if no filepath provided) or true | false depending on success
        """

        #Check if path exists and create if not
        path = self.setupDir(filepath)

        return df.to_csv(path+filename, **kwargs)
    #End writeCSV()