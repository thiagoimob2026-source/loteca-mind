import Link from "next/link";

export const metadata = {
  title: "Loteca Zebra 14 | Especialista Analítico",
  description: "Sistema analítico que cruza desempenho tático e inteligência de vestiário para gerar bilhetes otimizados de 14 pontos. Pare de perder dinheiro com achismos.",
  keywords: ["Loteca", "dicas loteca", "previsão de futebol", "análise de jogos", "14 pontos", "Zebra loteca"],
  openGraph: {
    title: "Loteca Zebra 14 | Especialista Analítico",
    description: "Método quantitativo e qualitativo para a Loteca.",
    type: "website",
  },
};

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#f8f9fc] theme-caixa text-slate-900 selection:bg-[#005CA9] selection:text-white pb-20">
      
      {/* Minimal Navbar */}
      <nav className="max-w-5xl mx-auto px-6 pt-8 pb-4 flex justify-between items-center border-b border-black/5">
        <div className="font-bold text-xl tracking-tight" style={{ fontFamily: "var(--font-outfit)" }}>
          Loteca Zebra 14
        </div>
        <Link href="/dashboard" className="text-sm font-medium hover:text-slate-500 transition-colors">
          Acessar Painel →
        </Link>
      </nav>

      <main className="max-w-3xl mx-auto px-6 pt-24 pb-12">
        
        {/* HERO SECTION - Typography Focused */}
        <section className="mb-24 animate-fade-in text-center sm:text-left">
          <p className="text-xs font-semibold tracking-widest text-slate-500 uppercase mb-6">
            Inteligência Analítica Aplicada
          </p>
          <h1 
            className="text-4xl sm:text-6xl font-extrabold leading-[1.1] tracking-tight mb-8"
            style={{ fontFamily: "var(--font-outfit)" }}
          >
            Aposte na estatística.<br />
            Antecipe o vestiário.
          </h1>
          <p className="text-lg sm:text-xl text-slate-600 font-medium leading-relaxed mb-10 max-w-2xl">
            A maioria dos apostadores joga dinheiro fora defendendo o próprio time ou chutando zebras improváveis. Transforme seus jogos usando nosso cruzamento de dados de campo (xG e Posse) com análise de pressões psicológicas do futebol brasileiro.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4">
            <Link 
              href="/dashboard" 
              className="bg-[#009B3A] text-white font-bold px-8 py-4 rounded-lg hover:bg-[#007A2D] transition-all shadow-lg hover:shadow-xl text-center"
            >
              Consultar Rodada Oficial
            </Link>
            <a 
              href="#metodologia" 
              className="bg-white text-slate-700 border border-slate-200 font-medium px-8 py-4 rounded-lg hover:border-slate-400 hover:bg-slate-50 transition-all text-center"
            >
              Entender a Metodologia
            </a>
          </div>
        </section>

        <hr className="border-t border-black/10 my-16" id="metodologia" />

        {/* METHODOLOGY DEEP DIVE SECTION */}
        <section className="mb-24">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4" style={{ fontFamily: "var(--font-outfit)" }}>
              As Duas Forças do Método Zebra 14
            </h2>
            <p className="text-slate-600 max-w-2xl mx-auto">
              Para vencer na Loteca, não basta olhar a tabela. Construímos nosso motor baseando-se em duas disciplinas acadêmicas para desviar das "análises frias" e do perigoso "efeito manada".
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Pilastra 1: Ciência de Dados */}
            <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm relative overflow-hidden group hover:border-[#005CA9] transition-colors">
              <div className="absolute top-0 right-0 p-4 opacity-10 text-6xl group-hover:scale-110 transition-transform">📈</div>
              <h3 className="text-xl font-bold mb-3 text-[#005CA9]">Ciência de Dados (Estatística Tática)</h3>
              <p className="text-sm text-slate-700 font-bold mb-4">O remédio contra o "Efeito Manada".</p>
              <p className="text-sm text-slate-600 leading-relaxed mb-4">
                Enquanto o povão aposta no time por causa da camisa ou do nome pesado, o nosso motor matemático analisa a <strong>Geração de Gols Esperados (xG)</strong>, posse de bola útil e eficiência de finalização profunda.
              </p>
              <ul className="text-sm text-slate-500 space-y-2">
                <li>• Ignora momento da camisa.</li>
                <li>• Foca em quem <span className="underline">realmente</span> domina o campo.</li>
                <li>• Revela times pequenos que estão subvalorizados.</li>
              </ul>
            </div>

            {/* Pilastra 2: Psicologia Esportiva */}
            <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm relative overflow-hidden group hover:border-[#DA291C] transition-colors">
              <div className="absolute top-0 right-0 p-4 opacity-10 text-6xl group-hover:scale-110 transition-transform">🧠</div>
              <div className="inline-flex items-center gap-1 bg-amber-100 text-amber-800 text-xs font-bold px-2 py-1 rounded mb-2">
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                Baseado em Literatura Científica
              </div>
              <h3 className="text-xl font-bold mb-3 text-[#DA291C]">Psicologia Escaneada (RAG)</h3>
              <p className="text-sm text-slate-700 font-bold mb-4">A vacina contra as "Análises Frias".</p>
              <p className="text-sm text-slate-600 leading-relaxed mb-4">
                Nosso motor lê automaticamente artigos científicos (como Li & Pan, 2025 e Jekauc, 2024) para interpretar o clima das notícias em tempo real que varremos sobre os times.
              </p>
              <ul className="text-sm text-slate-500 space-y-2">
                <li>• Aplica a Teoria da Espiral Descendente e Flow State.</li>
                <li>• Varredura semanal contra "Apostas Empurrada por Torcida".</li>
                <li>• Retira a probabilidade superestimada de times estrelados em crise.</li>
              </ul>
            </div>
          </div>
        </section>

        <hr className="border-t border-black/10 my-16" />

        {/* MECHANISM SECTION - The Before/After Concept */}
        <section className="mb-24">
          <h2 className="text-2xl font-bold mb-8" style={{ fontFamily: "var(--font-outfit)" }}>
            O Problema do Palpite Amador
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* O Padrão (Before) */}
            <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm opacity-80 hover:opacity-100 transition-opacity">
              <h3 className="font-bold text-lg mb-3">Abordagem Comum</h3>
              <ul className="space-y-4 text-sm text-slate-600">
                <li className="flex items-start gap-3">
                  <span className="text-slate-400">×</span>
                  Apostas guiadas por quem tem o maior nome ou a maior torcida.
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-slate-400">×</span>
                  Ignoram estatísticas subjacentes como Expected Goals (xG).
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-slate-400">×</span>
                  Não consideram Lei do Ex, Demissão de Técnico ou jogos de 6 pontos.
                </li>
              </ul>
            </div>

            {/* O Mecanismo Único (After) */}
            <div className="bg-[#005CA9] text-white p-8 rounded-xl shadow-xl transform transition-transform hover:-translate-y-1">
              <h3 className="font-bold text-lg mb-3">O Motor Loteca Zebra 14</h3>
              <ul className="space-y-4 text-sm text-slate-300">
                <li className="flex items-start gap-3">
                  <span className="text-emerald-400">✓</span>
                  <strong>Agente Tático:</strong> Calcula probabilidades precisas baseadas em eficiência real de jogo, não em fama.
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-emerald-400">✓</span>
                  <strong>Agente Psicológico (Científico):</strong> Escaneia a Internet e confronta com o banco de dados acadêmico (Teses e Papers) para definir o estado emocional de forma isenta.
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-emerald-400">✓</span>
                  <strong>Caçador de Zebras:</strong> Cruza os dois motores para avisar matematicamente onde a zebra vai passear.
                </li>
              </ul>
            </div>

          </div>
        </section>

        {/* PROOF & FINAL CTA */}
        <section className="bg-white p-10 rounded-2xl border border-slate-200 text-center shadow-sm">
          <h2 className="text-2xl font-bold mb-4" style={{ fontFamily: "var(--font-outfit)" }}>
            Pare de jogar na loteria às cegas
          </h2>
          <p className="text-slate-600 mb-8 max-w-md mx-auto">
            A matemática por trás do futebol é previsível. Os jogos do próximo concurso da Loteca já foram mapeados e as tendências já estão separadas.
          </p>
          <Link 
            href="/dashboard" 
            className="inline-block bg-[#009B3A] text-white font-bold px-8 py-4 rounded-lg hover:bg-[#007A2D] transition-all shadow-md"
          >
            Acessar Bilhetes e Probabilidades →
          </Link>
        </section>

      </main>

      {/* Very minimalist footer */}
      <footer className="text-center text-xs text-slate-400 mt-12 pb-8">
        &copy; {new Date().getFullYear()} Loteca Zebra 14. Análise Esportiva Inteligente.
      </footer>

    </div>
  );
}
