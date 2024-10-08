def main():
    print("query script execution")
    print("Ready to accept your question.")
    query = input("Enter your question: ")
    print("", flush=True)  # Force flushing the output buffer
   
    if query:
        vector_results = query_azure_search(query, 'vector')
        hybrid_results = query_azure_search(query, 'hybrid')
       
        print("Vector Search Results:")
        for result in vector_results:
            print(f"Title: {result['title']}")
            print(f"Chunk ID: {result['chunk_id']}")
            print(f"Parent ID: {result['parent_id']}")
            print(f"Score: {result['@search.score']}")
            print(f"Content: {result['chunk'][:100]}...\n")
       
        print("\nHybrid Search Results:")
        for result in hybrid_results:
            print(f"Title: {result['title']}")
            print(f"Chunk ID: {result['chunk_id']}")
            print(f"Parent ID: {result['parent_id']}")
            print(f"Score: {result['@search.score']}")
            print(f"Content: {result['chunk'][:100]}...\n")
       
        # Combine results for OpenAI query
        combined_results = vector_results + hybrid_results
       
        if combined_results:
            answer = query_azure_openai(query, combined_results)
            if answer:
                print("Answer about Employee Benefits:")
                print(answer)
                save_to_markdown(query, vector_results, hybrid_results, answer)
            else:
                logger.error("Failed to get a response from Azure OpenAI.")
        else:
            print("No search results found. Please check your index and query.")
    else:
        logger.warning("No query specified.")
 
if __name__ == "__main__":
    main()