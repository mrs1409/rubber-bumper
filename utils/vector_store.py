import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    """
    A simple in-memory vector store implementation using TF-IDF vectorization.
    With pre-loaded Rubber Bumper case study data.
    """
    
    def __init__(self):
        """Initialize the vector store with Rubber Bumper case study data."""
        self.documents = []
        self.vectorizer = TfidfVectorizer()
        self.vectors = None
        
        # Pre-load the Rubber Bumper case study information
        self.load_rubber_bumper_data()
        
    def load_rubber_bumper_data(self):
        """Load the Rubber Bumper case study data directly into the vector store."""
        rubber_bumper_documents = [
            """
            RUBBER BUMPER
            Rubber Bumper Co is a small family owned producer of rubber products. It 
            prides itself on producing a limited range of products but producing the 
            highest quality on the market. In general, new products are introduced after 
            much deliberation and careful market study. The company has recently 
            appointed a new President who noticed decreasing profits over the last 
            couple of years.
            """,
            
            """
            Clarifying Information:
            What type of products do they sell? The company only sells two products; rubber bands and 
            condoms.
            Is the company seeing similar declines in topline sales? Topline sales have remained relatively 
            stable over the last 3 years.
            What is Rubber Bumper's market position? Rubber Bumper is the market leader in both of their 
            product industries.
            """,
            
            """
            Rubber bands sold each year (millions of pounds of rubber):
            2011: Rubber Bumper: 4, Max Rubber: 17, Others (8): 9, Total: 30
            2012: Rubber Bumper: 3, Max Rubber: 19, Others (8): 9, Total: 31
            2013: Rubber Bumper: 3, Max Rubber: 21, Others (8): 8, Total: 32
            2014: Rubber Bumper: 2.5, Max Rubber: 21, Others (8): 7.5, Total: 31
            2015: Rubber Bumper: 2.5, Max Rubber: 22, Others (8): 6.5, Total: 31
            2016: Rubber Bumper: 2.5, Max Rubber: 23, Others (8): 4.5, Total: 30
            2017: Rubber Bumper: 2, Max Rubber: 24, Others (8): 5, Total: 31
            """,
            
            """
            Condoms sold each year (millions of condoms):
            2011: Rubber Bumper: 1, Spartan: 100, Durable: 150, Others (15): 99, Total: 350
            2012: Rubber Bumper: 2, Spartan: 110, Durable: 155, Others (15): 93, Total: 360
            2013: Rubber Bumper: 5, Spartan: 108, Durable: 152, Others (15): 105, Total: 370
            2014: Rubber Bumper: 10, Spartan: 115, Durable: 158, Others (15): 107, Total: 390
            2015: Rubber Bumper: 10, Spartan: 117, Durable: 159, Others (15): 119, Total: 405
            2016: Rubber Bumper: 10, Spartan: 115, Durable: 165, Others (15): 130, Total: 420
            2017: Rubber Bumper: 10, Spartan: 115, Durable: 170, Others (15): 155, Total: 450
            """,
            
            """
            Market Insights:
            1. The rubber band market is flat whereas the condom market is showing strong growth in the United States.
            2. The dominant player in the rubber band industry (Max Rubber) is gaining more and more market share.
            3. While the condom industry is growing (30% from 2005 to 2011) the major competitors are not growing as fast (~15% each).
            4. The condom industry is more fragmented than the rubber band industry, and the smaller players are getting a larger proportion of the market.
            """,
            
            """
            Rubber Band Factory Information:
            - They make boxes of 500 rubber bands that they sell to retailers for $20 a box.
            - 1 pound of rubber makes approximately 125 rubber bands.
            - The rubber band factory has an inclusive $4MM in annual overhead.
            - It costs $1 to turn a pound of rubber into a pound of rubber bands (assume no waste).
            """,
            
            """
            Condom Factory Information:
            - They sell 4 packs of condoms to retailers for $3 a pack.
            - The factory is smaller than the rubber band factory and only costs $2MM in annual overhead, inclusive of everything.
            - Each condom costs $0.10 to make.
            """,
            
            """
            Financial Calculations:
            Rubber Band Factory (2017):
            - 2MM lbs of rubber x 125 rubber bands/lb = 250MM rubber bands
            - 250MM rubber bands / 500 rubber bands/box = 500K boxes
            - 500K boxes x $20/box = $10MM in Revenue
            - 2MM lbs of rubber x $1/lb = $2MM in variable costs
            - Rubber Band Profit = $10MM - $2MM - $4MM = $4MM in profit
            
            Condom Factory (2017):
            - 10MM condoms / 4 condoms per pack = 2.5MM packs
            - 2.5MM packs x $3/pack = $7.5MM in Revenue
            - 10MM condoms x $0.10/condom = $1MM in variable costs
            - Condom Profit = $7.5MM - $1MM - $2MM = $4.5MM in profit
            """,
            
            """
            Plant Conversion Analysis:
            - It will cost $2MM dollars to refurbish the rubber band plant to make condoms.
            - The conversion would take 1 year to complete during which time the factory will be off-line.
            - During this time, Rubber Bumper won't be able to make any rubber bands.
            - The bigger plant can produce twice the volume of condoms as the smaller plant.
            - Rubber Bumper Co's payback period for such projects is 4 years.
            - Rubber Bumper's rubber band demand has stabilized at 2MM lbs per year.
            """,
            
            """
            Plant Conversion Financial Implications:
            - 1 year offline means losing ($10MM - $2MM) = $8MM in contribution.
            - Capital Expenditures = $2MM.
            - Total Cost of Project = $8MM + $2MM = $10MM.
            - The bigger factory can produce twice as many condoms: 10MM x 2 = 20MM condoms.
            - 20MM condoms / 4 condoms per pack = 5MM packs.
            - 5MM packs x $3/pack = $15MM in Revenue.
            - 20MM condoms x $0.10/condom = $2MM in variable costs.
            - New Condom Profit = $15MM - $2MM - $2MM = $11MM.
            - Current combined profit = $4MM (rubber bands) + $4.5MM (condoms) = $8.5MM.
            - After conversion: $11MM profit.
            - Incremental profit: $11MM - $8.5MM = $2.5MM per year.
            - Payback period: 1 year (offline) + ($10MM / $2.5MM) = 5 years.
            """,
            
            """
            Risks Involved with Plant Conversion:
            - Assumes that Rubber Bumper can sell 3x the number of condoms it sells today, immediately.
            - Assumes that rubber band demand won't rebound.
            - Political changes could affect market demand for condoms.
            - Less diversification in products exposes them to increased market risk.
            - Condoms are not as generic of a product as rubber bands and may require a larger investment in advertising.
            - Potentially more legal risk in selling contraception than rubber bands.
            - Employees may not want to make condoms or may need retraining.
            """,
            
            """
            Recommendation Summary:
            Based on the analysis, converting the rubber band factory to produce condoms would increase profitability in the long run,
            but the payback period of approximately 5 years exceeds the company's target of 4 years. Additionally, there are significant 
            risks in assuming the company can triple its condom sales immediately. The recommendation would be to first invest in market 
            research to verify demand for increased condom production, while also exploring ways to reduce conversion costs or time to 
            improve the project economics.
            """
        ]
        
        # Add the documents to the store
        self.add_documents(rubber_bumper_documents)
        
    def add_documents(self, documents):
        """
        Add documents to the vector store.
        
        Args:
            documents: A list of strings (document texts).
        """
        # Add to existing documents
        self.documents.extend(documents)
        
        # Recompute vectors for all documents
        self._update_vectors()
    
    def _update_vectors(self):
        """Update the vectors for all documents."""
        if not self.documents:
            self.vectors = None
            return
            
        # Fit and transform the documents
        self.vectors = self.vectorizer.fit_transform(self.documents)
    
    def search(self, query, top_k=3):
        """
        Search for documents similar to the query.
        
        Args:
            query: A string representing the search query.
            top_k: An integer representing the number of top documents to return.
            
        Returns:
            A list of tuples (document_text, similarity_score).
        """
        if not self.documents or self.vectors is None:
            return []
        
        # Transform query
        query_vector = self.vectorizer.transform([query])
        
        # Compute similarities
        similarities = cosine_similarity(query_vector, self.vectors)[0]
        
        # Get top-k documents
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Return top-k documents with their similarity scores
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Only include relevant results
                results.append((self.documents[idx], similarities[idx]))
        
        return results
    
    def clear(self):
        """Clear all documents from the vector store and reload the base data."""
        self.documents = []
        self.vectors = None
        self.load_rubber_bumper_data()
