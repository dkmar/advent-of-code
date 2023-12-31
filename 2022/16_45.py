import re, collections, functools, heapq
def day16(s, *, part2=False):  # With A*-like pruning.
  rate_of_node, dsts_of_node = {}, {}
  for line in s.splitlines():
    node, s_rate, *dsts = re.findall(r'([A-Z][A-Z]|[0-9]+)', line)
    rate_of_node[node] = int(s_rate)
    dsts_of_node[node] = dsts
  assert rate_of_node['AA'] == 0  # As observed in input.
  best_benefit_found = 0

  @functools.lru_cache(maxsize=None)
  def possible_paths(node):  # BFS to return {node2: time if rate[node2] > 0}.
    queue = collections.deque([(0, node)])
    result = {}
    while queue:
      distance, node = queue.popleft()
      for node2 in dsts_of_node[node]:
        if node2 not in result:
          result[node2] = distance + 2  # Add extra 1 for "time to turn on the valve".
          queue.append((distance + 1, node2))
    result = {node: time for node, time in result.items() if rate_of_node[node] > 0}
    return result

  # Given workers located at `nodes`, with a subset of `enabled` nodes, worker 0 idle,
  # and worker 1 still needing `other_working` time, compute the maximum benefit.
  # def compute_benefit(cur_benefit, time_left, enabled, nodes, other_working):
  #   nonlocal best_benefit_found
  #   benefit = cur_benefit
  #   for dst, time in possible_paths(nodes[0]).items():
  #     if dst not in enabled and time <= time_left:
  #       nodes2, time_left2, other_working2 = (
  #           ((nodes[1], dst), time_left - other_working, time - other_working)
  #           if other_working < time else
  #           ((dst, nodes[1]), time_left - time, other_working - time))
  #       cur_benefit2 = cur_benefit + (time_left - time) * rate_of_node[dst]
  #       optimistic_remaining = ((time_left * 2 - time - other_working + 3) * 40 if part2 else
  #                               (time_left - time + 3) * 60)
  #       if cur_benefit2 + optimistic_remaining < best_benefit_found:  # A*-like pruning.
  #         continue
  #       candidate = compute_benefit(
  #           cur_benefit2, time_left2, enabled | {dst}, nodes2, other_working2)
  #       benefit = max(benefit, candidate)
  #   best_benefit_found = max(best_benefit_found, benefit)
  #   return benefit
  def compute_benefit(cur_benefit, time_left, enabled, nodes, other_working, beam_size=3000):
    nonlocal best_benefit_found
    benefit = cur_benefit

    # Find the next set of nodes to explore using beam search.
    candidates = []
    min_seen = -1
    for dst, time in possible_paths(nodes[0]).items():
        if dst not in enabled and time <= time_left:
            nodes2 = (nodes[1], dst) if other_working < time else (dst, nodes[1])
            time_left2 = time_left - other_working if other_working < time else time_left - time
            other_working2 = time - other_working if other_working < time else other_working - time
            cur_benefit2 = cur_benefit + (time_left - time) * rate_of_node[dst]
            # optimistic_remaining = (
            #     (time_left * 2 - time - other_working + 3) * 40 if part2 else
            #     (time_left - time + 3) * 60
            # )
            # if cur_benefit2 + optimistic_remaining < best_benefit_found:  # A*-like pruning.
            #     continue
            if min_seen == -1:
              min_seen = cur_benefit2
            elif cur_benefit2 < min_seen:
              continue
            
            candidates.append((cur_benefit2, time_left2, enabled | {dst}, nodes2, other_working2))
    
    candidates = heapq.nlargest(beam_size, candidates)

    # Recursively compute the maximum benefit for each candidate.
    for candidate in candidates:
        cur_benefit2, time_left2, enabled2, nodes2, other_working2 = candidate
        candidate_benefit = compute_benefit(
            cur_benefit2, time_left2, enabled2, nodes2, other_working2, beam_size
        )
        benefit = max(benefit, candidate_benefit)
    best_benefit_found = max(best_benefit_found, benefit)
    return benefit



  return compute_benefit(0, 26 if part2 else 30, set(), ('AA', 'AA'), 0 if part2 else 99)

with open('16.in', 'r') as f:
  print(day16(f.read(), part2=True))