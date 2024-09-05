const searchInput = document.getElementById("search-input");
const searchButton = document.getElementById("search-button");
const resultsContainer = document.getElementById("results");

const performSearch = async () => {
  const searchTerm = searchInput.value.trim().toLowerCase();
  if (!searchInput || searchTerm === "") {
    alert("Veuillez entrer un terme pour effectuer une recherche.");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5003/api/terms");
    const data = await response.json();
    // console.log(data);

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
};

searchButton.addEventListener("click", performSearch);
searchInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    performSearch();
  }
});

const displayResults = (results) => {
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
    <h4 class="">
      Sous-domaine :
      ${displaySubdomains("Sous-domaine", item.subdomains_fr)}
    </h4>
  </div>
  <div class="flow-root">
    <ul role="list" class="divide-y divide-gray-200">
      ${displayIfExists("Variante", item.variant_fr)}
      ${displayIfExists("Synonyme", item.near_synonym_fr)}
      ${displayIfExists("Définition", item.definition_fr)}
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex flex-col min-w-0">
            <p class="text-sm text-gray-500">Cooccurrence syntaxique</p>
            ${displayCooccurrence("Cooccurrence Syntaxique", item.syntactic_cooccurrence_fr)}
          </div>
        </div>
      </li>
      ${displayLexicalRelations("Relations lexicales", item.lexical_relations_fr)}
      ${displayIfExists("Note", item.note_fr)}
      ${displayIfExists("À ne pas confondre avec", item.note_to_be_confused_with_fr)}
      ${displayIfExists("Expression fréquente", item.frequent_expression_fr)}
      ${displayIfExists("Phraséologie", item.phraseology_fr)}
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
      ${displaySubdomains("Sous-domaine", item.subdomains_en)}
    </h4>
  </div>
  <div class="flow-root">
    <ul role="list" class="divide-y divide-gray-200">
      ${displayIfExists("Variant", item.variant_en)}
      ${displayIfExists("Synonym", item.near_synonym_en)}
      ${displayIfExists("Definition", item.definition_en)}
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex flex-col min-w-0">
            <p class="text-sm text-gray-500">Syntactic Cooccurrence</p>
            ${displayCooccurrence("Syntactic Cooccurrence", item.syntactic_cooccurrence_en)}
          </div>
        </div>
      </li>
      ${displayLexicalRelations("Lexical Relations", item.lexical_relations_en)}
      ${displayIfExists("Note", item.note_en)}
      ${displayIfExists("Not to be confused with", item.note_to_be_confused_with_en)}
      ${displayIfExists("Frequent expression", item.frequent_expression_en)}
      ${displayIfExists("Phraseology", item.phraseology_en)}
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
};

const displayIfExists = (label, value) => {
  if (value && value.trim() !== "") {
    return `
      <li class="py-3 sm:py-4">
        <div class="flex items-center space-x-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500">${label}</p>
            <p class="text-md font-medium text-gray-900">${value}</p>
          </div>
        </div>
      </li>`;
  }
  return "";
};

const displayLexicalRelations = (label, relations) => {
  if (Array.isArray(relations) && relations.length > 0) {
    return relations
      .map((relation) =>
        Object.keys(relation)
          .map((key) => {
            // console.log(`Relation key: ${key}, values: ${relation[key]}`);
            if (Array.isArray(relation[key])) {
              return `
                <li class="py-3 sm:py-4">
                  <div class="flex items-center space-x-4">
                    <div class="flex-1 min-w-0">
                      <p class="text-sm text-gray-500">${label} (${key})</p>
                      <p class="text-md font-medium text-gray-900">${relation[key].join(", ")}</p>
                    </div>
                  </div>
                </li>`;
            }
            return "";
          })
          .join(""),
      )
      .join("");
  }
  return "";
};

const displaySubdomains = (label, subdomains) => {
  const colors = [
    { text: "text-white", bg: "bg-[#296F9A]" },
    { text: "text-white", bg: "bg-[#A32A34]" },
    { text: "text-white", bg: "bg-black" },
  ];

  return subdomains
    .map((item, index) => {
      const color = colors[index % colors.length];
      return `
        <span class="inline-block ${color.bg} ${color.text} py-1 px-2 mr-1 mb-2 rounded-lg text-sm">${item}</span>
      `;
    })
    .join("");
};

const displayCooccurrence = (label, cooccurrence) => {
  return cooccurrence
    .map((item, index) => {
      return `<span class="mb-0">${item || "<br />"}</span>`;
    })
    .join("");
};

