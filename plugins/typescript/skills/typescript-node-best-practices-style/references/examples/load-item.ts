/* Node.js Best Practices: [1.2] domain stays independent of transport;
   [1.6] simple types; [2.12] return await retains async context;
   [3.12] named arrow expressions. Call with an already validated ID. */
import { AppError } from './app-error.ts';

export interface Item {
  id: string;
  title: string;
}

export interface ItemRepository {
  find(id: string): Promise<Item | undefined>;
}

const requireItem = async (
  id: string,
  repository: ItemRepository,
): Promise<Item> => {
  const item = await repository.find(id);
  if (item === undefined) {
    throw new AppError('ITEM_NOT_FOUND', 'The item is unavailable.', true);
  }
  return item;
};

export const loadItem = async (
  id: string,
  repository: ItemRepository,
): Promise<Item> => {
  return await requireItem(id, repository);
};
