import axios from "axios";

export interface SearchResult {
  _id: string;
  content: string;
}

export const getSearchResults = async (
  dataset: string,
  page: string,
  query: string
) => {
  try {
    const { data } = await axios.post("http://localhost:8000/search", {
      dataset: dataset.toLowerCase(),
      page: parseInt(page) + 1,
      query,
      optimized: false,
    });
    return data.search_results.search_results;
  } catch (err) {
    return [];
  }
};

export const getQuerySuggestion = async (dataset: string, query: string) => {
  try {
    const { data } = await axios.post(
      "http://localhost:8000/query-suggestion",
      {
        dataset: `${dataset.toLowerCase()}_queries`,
        query,
      }
    );
    return data.search_results.search_results;
  } catch (err) {
    return [];
  }
};
