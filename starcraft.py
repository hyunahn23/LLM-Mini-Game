import random
import time
from collections import Counter, defaultdict
import ollama

players = [
    "짐 레이너", "사라 케리건", "사미르 듀란", "에드먼드 듀크",
    "아크튜러스 멩스크", "톰 카잔스키", "노바 테라", "알렉세이 스투코프"
]

rooms = [
    '야마토 포 (Yamato Cannon)', '선원 편의 시설 (Crew Facilities)', '레이저 포 (Gun Batteries)',
    '차원 추진기 (Wrap Drive)', '핵융합 반응로 (Fusion Reactor)', '의무실 (Medical Room)',
    "캡틴룸 (Captain's Room)"
]

story_prompts = [
    "노바 테라가 조종당하고 있다는 보고가 있다. 감정 없이 움직이는 그녀의 태도는 그 자체로 위협이다.",
    "짐 레이너는 모두가 믿는 영웅이다. 하지만 그가 감염되었다면 아무도 의심하지 않을 것이다.",
    "케리건은 과거에 저그의 손에 넘어간 적이 있다. 그 기억이 되살아난다면...",
    "아크튜러스 멩스크의 정치적 수완이라면, 감염조차도 통치 도구로 활용할 수 있을 것이다.",
    "듀란은 이중첩자일 가능성이 크다. 감염자라면 그가 아닐 리 없다.",
    "듀크는 충성심 강한 장군이다. 그러나 감염된 충성은 가장 무섭다.",
    "톰 카잔스키는 단순하고 직설적인 인물이다. 하지만 때로는 그 단순함이 위장일 수도 있다.",
    "스투코프는 규율의 화신이다. 하지만 그 질서 속에 침투한 감염이라면 아무도 모를 것이다.",
    "노바의 사이오닉 통제가 약해지고 있다. 이상한 꿈을 꿨다는 보고가 들어왔다.",
    "듀란은 인간이 아닐지도 모른다. 그의 행동은 계산된 듯이 정밀하다.",
     "짐 레이너가 누군가와 속닥이며 의심스러운 무전을 나누는 것이 목격되었다.",
    "노바 테라의 사이오닉 신호가 일정하지 않다. 정신적 침투의 징후일 수도 있다.",
    "듀란은 매일 기록을 남기고 있다. 그러나 아무도 그 기록을 본 적이 없다.",
    "스투코프의 명령 체계는 변하지 않았지만, 감정이 배제된 것처럼 보인다.",
    "듀크 장군은 이상하리만치 조용하다. 전례 없는 태도 변화다.",
    "톰 카잔스키는 방어 시스템을 우연히 꺼트린 후 기억이 없다고 주장했다.",
    "케리건의 손목 장치에서 저그 신호와 유사한 주파수가 감지되었다.",
    "맹크스는 투표 시스템을 자신이 제어하고 있다고 은근히 암시했다.",
    "사령부 통신 로그에서 레이너의 음성이 기이하게 변조된 채 반복되었다.",
    "듀란의 공간 이동 로그가 실제 위치 기록과 불일치한다.",
    "노바가 감시 카메라를 모두 비활성화한 직후 한 명이 실종되었다.",
    "듀크는 동료의 죽음을 '군사적 불가피함'이라며 정당화했다.",
    "스투코프는 자꾸 과거 전쟁 이야기를 반복하며 현재를 부정하고 있다.",
    "톰은 지나치게 침착하다. 그다운 과민반응이 전혀 보이지 않는다.",
    "맹크스는 자신만 면역이라며 의료검사를 거부했다.",
    "레이너는 케리건을 두둔하는 발언을 반복하고 있다. 감정인가, 공모인가?",
    "듀란은 늘 중립적이다. 너무 완벽한 중립은 의심스럽다.",
    "노바는 동일 발언을 2일 연속 반복했다. 기억 조작 가능성이 있다.",
    "스투코프는 차트에 없는 장소에서 작전을 펼쳤다고 주장했다.",
    "케리건은 저그와 관련된 꿈을 꾸었다고 털어놓았다.",
    "듀크는 절차를 따르지 않고 무단 투표를 지시했다.",
    "맹크스는 자신을 감염자로 지목한 자를 전부 '반역자'로 선언했다.",
    "톰은 누군가를 몰래 감시한 사실을 인정했다. 이유는 말하지 않았다.",
    "듀란은 감염 상태에서도 정상이었을 수 있다는 가설을 주장했다.",
    "레이너는 '이제 믿을 사람은 없다'고 말하며 독립 행동을 시작했다.",
    "노바는 진단서 위조 가능성이 있다는 익명 제보가 들어왔다.",
    "듀크는 추방된 감염자가 '위대한 병기'였다고 칭했다.",
    "스투코프는 고립된 방에서 3시간 동안 홀로 있었다.",
    "케리건은 격납고를 봉쇄했다. 이유는 '예지몽 때문'이라고 했다.",
    "듀란은 '혼란이 곧 질서'라는 말을 자주 반복하고 있다.",
    "톰은 '직감'이라는 말을 근거 없이 반복하며 특정 인물을 몰아간다.",
    "맹크스는 정기 브리핑을 모두 생략하고 개인 조사에 집중하고 있다.",
    "레이너는 잠든 사이 꿈에서 감염자와 대화를 나눴다고 말했다.",
    "노바는 통신 장비를 자신의 것으로만 암호화해 사용하고 있다.",
    "스투코프는 어느 순간부터 주변의 질문에 대답하지 않는다.",
    "듀크는 '한 명쯤 희생되어야 진실이 드러난다'고 말했다.",
    "듀란은 투표 때마다 항상 특정 인물에게 표를 던진다. 이유는 모른다.",
    "케리건은 특정 구역의 접근을 강하게 막고 있다. 이유를 묻자 침묵했다.",
    "톰은 갑자기 다른 사람을 의심하지 않고 자책하는 태도로 변했다.",
    "맹크스는 '이 모든 혼란은 오히려 기회다'라고 말하며 웃었다."    "노바 테라가 조종당하고 있다는 보고가 있다. 감정 없이 움직이는 그녀의 태도는 그 자체로 위협이다.",
    "짐 레이너는 모두가 믿는 영웅이다. 하지만 그가 감염되었다면 아무도 의심하지 않을 것이다.",
    "케리건은 과거에 저그의 손에 넘어간 적이 있다. 그 기억이 되살아난다면...",
    "아크튜러스 멩스크의 정치적 수완이라면, 감염조차도 통치 도구로 활용할 수 있을 것이다.",
    "듀란은 이중첩자일 가능성이 크다. 감염자라면 그가 아닐 리 없다.",
    "듀크는 충성심 강한 장군이다. 그러나 감염된 충성은 가장 무섭다.",
    "톰 카잔스키는 단순하고 직설적인 인물이다. 하지만 때로는 그 단순함이 위장일 수도 있다.",
    "스투코프는 규율의 화신이다. 하지만 그 질서 속에 침투한 감염이라면 아무도 모를 것이다.",
    "노바의 사이오닉 통제가 약해지고 있다. 이상한 꿈을 꿨다는 보고가 들어왔다.",
    "듀란은 인간이 아닐지도 모른다. 그의 행동은 계산된 듯이 정밀하다.",
     "짐 레이너가 누군가와 속닥이며 의심스러운 무전을 나누는 것이 목격되었다.",
    "노바 테라의 사이오닉 신호가 일정하지 않다. 정신적 침투의 징후일 수도 있다.",
    "듀란은 매일 기록을 남기고 있다. 그러나 아무도 그 기록을 본 적이 없다.",
    "스투코프의 명령 체계는 변하지 않았지만, 감정이 배제된 것처럼 보인다.",
    "듀크 장군은 이상하리만치 조용하다. 전례 없는 태도 변화다.",
    "톰 카잔스키는 방어 시스템을 우연히 꺼트린 후 기억이 없다고 주장했다.",
    "케리건의 손목 장치에서 저그 신호와 유사한 주파수가 감지되었다.",
    "맹크스는 투표 시스템을 자신이 제어하고 있다고 은근히 암시했다.",
    "사령부 통신 로그에서 레이너의 음성이 기이하게 변조된 채 반복되었다.",
    "듀란의 공간 이동 로그가 실제 위치 기록과 불일치한다.",
    "노바가 감시 카메라를 모두 비활성화한 직후 한 명이 실종되었다.",
    "듀크는 동료의 죽음을 '군사적 불가피함'이라며 정당화했다.",
    "스투코프는 자꾸 과거 전쟁 이야기를 반복하며 현재를 부정하고 있다.",
    "톰은 지나치게 침착하다. 그다운 과민반응이 전혀 보이지 않는다.",
    "맹크스는 자신만 면역이라며 의료검사를 거부했다.",
    "레이너는 케리건을 두둔하는 발언을 반복하고 있다. 감정인가, 공모인가?",
    "듀란은 늘 중립적이다. 너무 완벽한 중립은 의심스럽다.",
    "노바는 동일 발언을 2일 연속 반복했다. 기억 조작 가능성이 있다.",
    "스투코프는 차트에 없는 장소에서 작전을 펼쳤다고 주장했다.",
    "케리건은 저그와 관련된 꿈을 꾸었다고 털어놓았다.",
    "듀크는 절차를 따르지 않고 무단 투표를 지시했다.",
    "맹크스는 자신을 감염자로 지목한 자를 전부 '반역자'로 선언했다.",
    "톰은 누군가를 몰래 감시한 사실을 인정했다. 이유는 말하지 않았다.",
    "듀란은 감염 상태에서도 정상이었을 수 있다는 가설을 주장했다.",
    "레이너는 '이제 믿을 사람은 없다'고 말하며 독립 행동을 시작했다.",
    "노바는 진단서 위조 가능성이 있다는 익명 제보가 들어왔다.",
    "듀크는 추방된 감염자가 '위대한 병기'였다고 칭했다.",
    "스투코프는 고립된 방에서 3시간 동안 홀로 있었다.",
    "케리건은 격납고를 봉쇄했다. 이유는 '예지몽 때문'이라고 했다.",
    "듀란은 '혼란이 곧 질서'라는 말을 자주 반복하고 있다.",
    "톰은 '직감'이라는 말을 근거 없이 반복하며 특정 인물을 몰아간다.",
    "맹크스는 정기 브리핑을 모두 생략하고 개인 조사에 집중하고 있다.",
    "레이너는 잠든 사이 꿈에서 감염자와 대화를 나눴다고 말했다.",
    "노바는 통신 장비를 자신의 것으로만 암호화해 사용하고 있다.",
    "스투코프는 어느 순간부터 주변의 질문에 대답하지 않는다.",
    "듀크는 '한 명쯤 희생되어야 진실이 드러난다'고 말했다.",
    "듀란은 투표 때마다 항상 특정 인물에게 표를 던진다. 이유는 모른다.",
    "케리건은 특정 구역의 접근을 강하게 막고 있다. 이유를 묻자 침묵했다.",
    "톰은 갑자기 다른 사람을 의심하지 않고 자책하는 태도로 변했다.",
    "맹크스는 '이 모든 혼란은 오히려 기회다'라고 말하며 웃었다."
]

role_descriptions = {
    '테란': '당신은 테란입니다. 감염된 테란을 찾아내야 합니다.',
    '감염된 테란': '당신은 감염된 테란입니다. 감염되지 않은척 하여 끝까지 살아남으세요.',
    '사망': '당신은 사망했지만 유령으로 단서를 남길 수 있습니다.'
}

imposter_lies = [
    "{room}에서 {target}와 같이 있었고 이상한 점은 없었어요.",
    "{target}는 {room}에 있었어요. 급하게 나가던데요?",
    "선원 편의 시설에서 {target}의 움직임이 수상했어요.",
    "정비 중에 {target}가 {room} 쪽에서 나왔어요. 아무 말도 안 했어요."
]
crew_truths = [
    "{target}가 {room} 근처에 있었어요. 아무도 없는데 혼자였어요.",
    "{room}에서 이상한 소리가 났고 {target}가 있었어요.",
    "저는 {room}에 있었는데 {target}가 갑자기 사라졌어요.",
    "{target}가 선원 편의 시설 쪽에서 몰래 나가는 걸 봤어요."
]

memory_log = defaultdict(list)
suspicion_score = defaultdict(int)
elimination_history = []
personal_messages = {}
emotion_state = defaultdict(lambda: "기본")


def run_intro():
    story = random.choice(story_prompts)
    print("\n🚀 Good day, Commander. 배틀크루저에 오신 것을 환영합니다!")
    print("🧠 감염된 테란이 우리 승무원 사이에 숨어 있습니다.")
    print("🦠 저그의 퀸과 디바우러가 침투하여 선원 중 한 명을 감염시켰습니다.")
    print("📖 스토리: " + story)
    print("🎯 투표를 통해 매일 한 명씩 우주 밖으로 추방하십시오.")
    input("▶️ 엔터를 눌러 DAY 1을 시작하세요...")


def generate_roles():
    roles = {p: '테란' for p in players}
    imposter = random.choice(players)
    roles[imposter] = '감염된 테란'
    return roles, imposter


def run_day1_intro(roles):
    print("\n☀️ DAY 1: 테란 자기소개 시간입니다.")
    for pid in players:
        prompt = f"{pid}라는 이름의 테란으로, 저그로 감염되지 않았다고 증명하기 위해, 이와 관련하여 신뢰를 얻기 위한 간단한 자기소개를 한줄로 하세요."
        response = ollama.chat(model='EEVE-Korean-10.8B', messages=[{"role": "user", "content": prompt}], stream=True)
        print(f"🤖 [{pid}]: ", end='', flush=True)
        for chunk in response:
            print(chunk.get("message", {}).get("content", ''), end='', flush=True)
        print()
    input("\n▶️ 엔터를 눌러 DAY 2를 시작하세요...")


def generate_clues(roles):
    clues = {}
    for p in players:
        clues[p] = {'기억': []}
        target = random.choice([x for x in players if x != p])
        room = random.choice(rooms)
        if roles[p] == '감염된 테란':
            line = random.choice(imposter_lies).format(target=target, room=room)
            line += f" (설득력: {random.randint(7, 10)}/10)"
        else:
            line = random.choice(crew_truths).format(target=target, room=room)
            line += f" (의무실 진단: {'정상' if random.random() > 0.2 else '이상 감지'})"
        clues[p]['기억'].append(line)
    return clues


def run_talk_round(alive, roles, clues):
    print("\n🧠 사령관, 테란들의 진술을 들어보십시오.")
    statements = {}

    persona_prompts = {
        "아크튜러스 멩스크": "당신은 야망 있는 독재자입니다. 고상한 말투로 대중을 선동하고, 권위적으로 말하세요.",
        "짐 레이너": "당신은 자유와 정의를 중시하는 전직 보안관입니다. 냉소적 유머를 섞되 인간적인 따뜻함을 유지하세요.",
        "사라 케리건": "당신은 고통을 겪은 유령 요원입니다. 침착하고 단호하며 감정을 억누르는 말투를 사용하세요.",
        "사미르 듀란": "당신은 침착하고 이중적인 전략가입니다. 교묘한 말로 상대의 의심을 유도하세요.",
        "에드먼드 듀크": "당신은 원칙주의 장군입니다. 냉정하고 분석적인 말투로 발언하세요.",
        "톰 카잔스키": "당신은 직설적이고 터프한 실전형입니다. 투박하고 솔직하게 말하세요.",
        "노바 테라": "당신은 냉정한 유령 요원입니다. 감정을 배제한 간결하고 정확한 문장을 사용하세요.",
        "알렉세이 스투코프": "당신은 명예를 중시하는 해군 전략가입니다. 고풍스럽고 품위 있게 말하세요."
    }

    emotion_tone = {
        "기본": "",
        "불안": "당신은 최근 의심을 받아 불안한 상태입니다.",
        "슬픔": "당신은 동료의 추방으로 슬픔에 잠겨 있습니다.",
        "분노": "당신은 누군가에게 강한 분노를 느끼고 있습니다.",
        "체념": "당신은 체념한 상태로 무기력하게 말합니다."
    }

    def update_emotion_state(pid):
        if suspicion_score[pid] >= 2:
            return "불안"
        if elimination_history:
            last = elimination_history[-1]
            if last[0] != pid:
                return "슬픔" if last[1] != "감염된 테란" else "분노"
        return "기본"

    for pid in alive:
        memory = '\n'.join(f"- {m}" for m in clues[pid]['기억'])
        if memory in memory_log[pid]:
            suspicion_score[pid] += 1
        memory_log[pid].append(memory)

        emotion_state[pid] = update_emotion_state(pid)
        emotion_line = emotion_tone.get(emotion_state[pid], "")
        persona = persona_prompts.get(pid, "당신은 테란 병사입니다.")

        prompt = f"""
저는 {pid}입니다. {persona}
{emotion_line}

현재 상황에서 저는 감염되지 않았습니다.
단서는 다음과 같습니다:
{memory}
한 문장으로 주장 또는 타인을 의심하세요.
형식: 발언 + (비밀 메시지: 내용)
"""

        print(f"🤖 [{pid}]: ", end='', flush=True)
        response = ollama.chat(model='EEVE-Korean-10.8B', messages=[{"role": "user", "content": prompt}], stream=True)
        msg = ''
        for chunk in response:
            content = chunk.get("message", {}).get("content", '')
            print(content, end='', flush=True)
            msg += content
        print()

        if '(비밀 메시지:' in msg:
            try:
                secret = msg.split('(비밀 메시지:')[1].split(')')[0].strip()
                personal_messages[pid] = secret
            except:
                pass
        statements[pid] = msg

    print("\n📩 개인 메시지 도착:")
    for pid, msg in personal_messages.items():
        if pid in alive:
            print(f"- {pid}: '{msg}'")
    return statements


def resolve_tie_vote(candidates):
    print(f"\n🤔 동표입니다. 후보: {', '.join(candidates)}")
    user_final = input(f"최종 배출 대상자 선택 ({'/'.join(candidates)}): ").strip()
    while user_final not in candidates:
        user_final = input("❗ 올바른 이름을 다시 입력하세요: ").strip()
    return user_final


def run_vote_phase(alive, roles):
    vote = input("\n🗳️ 누구를 우주 밖으로 추방하시겠습니까? (테란 이름 입력): ").strip()
    while vote not in alive:
        vote = input("❗ 올바른 테란 이름을 다시 입력하세요: ").strip()
    votes = [random.choice([p for p in alive if p != vote]) for _ in range(len(alive)-2)] + [vote]
    count = Counter(votes)
    sorted_votes = count.most_common()

    print("\n📊 투표 결과:")
    for pid, v in sorted_votes:
        print(f"{pid}: {'■'*v} ({v}표)")

    top_votes = sorted_votes[0][1]
    top_candidates = [pid for pid, v in sorted_votes if v == top_votes]
    eliminated = resolve_tie_vote(top_candidates) if len(top_candidates) > 1 else sorted_votes[0][0]

    role = roles[eliminated]
    elimination_history.append((eliminated, role))
    print(f"\n💥 {eliminated}는 우주 밖으로 추방되었습니다. (정체: {'감염된 테란' if role == '감염된 테란' else '선량한 테란'})")
    return eliminated


def check_win(alive, roles):
    remaining = [p for p in alive if roles[p] != '사망']
    imposters = [p for p in remaining if roles[p] == '감염된 테란']
    if not imposters:
        return '✅ 테란 승리!'
    if len(remaining) <= 2:
        return '💀 저그 승리!'
    return None


def show_final_report(roles):
    print("\n📊 최종 분석 리포트\n----------------------")
    for name, score in sorted(suspicion_score.items(), key=lambda x: -x[1]):
        print(f"{name}: 의심 수치 {score}")
    correct_guesses = [e for e in elimination_history if e[1] == '감염된 테란']
    print(f"\n🧩 추리 정확도 평가:")
    print(f"정확히 추방한 감염된 테란 수: {len(correct_guesses)}")
    print(f"총 추방 수: {len(elimination_history)}")
    acc = len(correct_guesses) / len(elimination_history) * 100 if elimination_history else 0
    print(f"추리 정확도: {acc:.1f}%")


def run_game():
    run_intro()
    roles, imposter = generate_roles()
    run_day1_intro(roles)
    alive = players.copy()
    day = 2
    while True:
        print(f"\n☀️ DAY {day}:")
        print(f"남은 인원: {len(alive)}명 | 감염된 테란 생존 여부: {'생존' if any(roles[p]=='감염된 테란' for p in alive) else '전멸'}")
        clues = generate_clues(roles)
        run_talk_round(alive, roles, clues)
        eliminated = run_vote_phase(alive, roles)
        alive.remove(eliminated)
        roles[eliminated] = '사망'
        result = check_win(alive, roles)
        if result:
            print(f"\n🏁 게임 종료: {result}")
            show_final_report(roles)
            break
        day += 1


if __name__ == '__main__':
    run_game()