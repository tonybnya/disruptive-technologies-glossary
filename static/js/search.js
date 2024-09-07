const searchInput = document.getElementById("search-input");
const searchButton = document.getElementById("search-button");
const resultsContainer = document.getElementById("results");

searchButton.addEventListener("click", performSearch);
searchInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    performSearch();
  }
});

async function performSearch() {
  const searchTerm = searchInput.value.trim().toLowerCase();
  if (!searchInput || searchTerm === "") {
    alert("Veuillez entrer un terme pour effectuer une recherche.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5003/api/terms");
    const data = await response.json();
    console.log(data);

    const filteredResults = data.filter(
      (item) =>
        item.french_term.toLowerCase().includes(searchTerm) ||
        item.english_term.toLowerCase().includes(searchTerm),
    );

    displayResults(filteredResults);
  } catch (error) {
    alert("Vérifiez l'orthographe du terme et Réessayez !");
    console.error("Error fetching data:", error);
    resultsContainer.innerHTML = `<p>Erreur dans l'obtention des résultats. Veuillez réessayer.</p>`;
  }
}

function displayResults(results) {
  console.log(typeof results);
  if (results.length === 0) {
    resultsContainer.innerHTML = "<p>Aucun résultat trouvé.</p>";
    return;
  }

  resultsContainer.innerHTML = results
    .map(
      (item) => `
<div class="bg-white shadow-lg rounded-lg mb-4 p-4 sm:p-6 h-full">
  <div class="flex flex-col items-start gap-1 mb-4">
    <h3 class="text-xl max-sm:text-lg font-bold leading-none text-gray-500">
      Terme en Français :
      <span class="text-[#A32A34]">${item.french_term}</span>
    </h3>
    <h4 class="text-gray-700">
      Domaine :
      <span class="text-[#296F9A]">${item.domain_fr}</span>
    </h4>
    <h4 class="text-gray-700">
      Sous-domaine :
      <span class="text-[#296F9A]">${item.subdomains_fr}</span>
    </h4>
  </div>
  <div class="flow-root">
    <ul role="list" class="divide-y divide-gray-200">
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Variante</p>
            <p class="text-md font-medium text-gray-900">${item.variant_fr}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Synonyme</p>
            <p class="text-md font-medium text-gray-900">${item.near_synonym_fr}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Définition</p>
            <p class="text-md font-medium text-gray-900">${item.definition_fr}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Cooccurrence syntaxique</p>
            <p class="text-md font-medium text-gray-900">${item.syntactic_cooccurrence_fr}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Relations lexicales</p>
            <p class="text-md font-medium text-gray-900">${item.lexical_relations_fr}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Note</p>
            <p class="text-md font-medium text-gray-900">${item.note_fr}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">À ne pas confondre avec</p>
            <p class="text-md font-medium text-gray-900">${item.note_to_be_confused_with_fr}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Expression fréquente</p>
            <p class="text-md font-medium text-gray-900">${item.frequent_expression_fr}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Phraséologie</p>
            <p class="text-md font-medium text-gray-900">${item.phraseology_fr}</p>
          </div>
        </div>
      </li>
      <li class="pt-3 sm:pt-4 pb-0">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Contexte</p>
            <p class="text-md font-medium text-gray-900">${item.context_fr}</p>
          </div>
        </div>
      </li>
    </ul>
  </div>
</div>
<!---->
<div class="bg-white shadow-lg rounded-lg mb-4 p-4 sm:p-6 h-full">
  <div class="flex flex-col items-start gap-1 mb-4">
    <h3 class="text-xl max-sm:text-lg font-bold leading-none text-gray-500">
      English Term:
      <span class="text-[#A32A34]">${item.english_term}</span>
    </h3>
    <h4 class="text-gray-700">
      Domain:
      <span class="text-[#296F9A]">${item.domain_en}</span>
    </h4>
    <h4 class="text-gray-700">
      Subdomain:
      <span class="text-[#296F9A]">${item.subdomains_en}</span>
    </h4>
  </div>
  <div class="flow-root">
    <ul role="list" class="divide-y divide-gray-200">
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Variant</p>
            <p class="text-md font-medium text-gray-900">${item.variant_en}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Synonym</p>
            <p class="text-md font-medium text-gray-900">${item.near_synonym_en}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Definition</p>
            <p class="text-md font-medium text-gray-900">${item.definition_en}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Syntactic Cooccurrence</p>
            <p class="text-md font-medium text-gray-900">${item.syntactic_cooccurrence_en}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Lexical Relations</p>
            <p class="text-md font-medium text-gray-900">${item.lexical_relations_en}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Note</p>
            <p class="text-md font-medium text-gray-900">${item.note_en}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Not to be confused with</p>
            <p class="text-md font-medium text-gray-900">${item.note_to_be_confused_with_en}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Frequent Expression</p>
            <p class="text-md font-medium text-gray-900">${item.frequent_expression_en}</p>
          </div>
        </div>
      </li>
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Phraseology</p>
            <p class="text-md font-medium text-gray-900">${item.phraseology_en}</p>
          </div>
        </div>
      </li>
      <li class="pt-3 sm:pt-4 pb-0">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">Context</p>
            <p class="text-md font-medium text-gray-900">${item.context_en}</p>
          </div>
        </div>
      </li>
    </ul>
  </div>
</div>
`,
    )
    .join("");

  document.getElementById("search-input").value = "";
}
